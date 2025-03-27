"""
Base Data Transfer Object for ActiveTrail API.
"""

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Optional, ClassVar, List, Type, TypeVar, cast
import json
import re
from datetime import datetime

T = TypeVar('T', bound='BaseDTO')

@dataclass
class BaseDTO:
    """
    Base class for all DTOs in the ActiveTrail API.
    
    This class provides common functionality for all DTOs, such as:
    - Converting to dictionary for API requests
    - Creating DTOs from API responses
    - JSON serialization and deserialization
    """
    
    # Class variables for field mappings and optional fields
    _api_field_mapping: ClassVar[Dict[str, str]] = {}
    _optional_fields: ClassVar[List[str]] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DTO to a dictionary for API requests.
        
        Returns:
            Dict[str, Any]: Dictionary representation suitable for API requests
        """
        # Get all non-None fields
        result = {}
        data = asdict(self)
        
        # Apply field mappings and filter out None values
        for field_name, value in data.items():
            if value is None and field_name in self._optional_fields:
                continue
                
            # Apply field mapping if it exists
            api_field_name = self._api_field_mapping.get(field_name, field_name)
            
            # Handle different types of values
            if isinstance(value, datetime):
                # Convert datetime to ISO format string
                result[api_field_name] = value.isoformat()
            elif isinstance(value, BaseDTO):
                # Convert nested DTO to dictionary
                result[api_field_name] = value.to_dict()
            elif isinstance(value, list):
                # Process list items
                if value and all(isinstance(item, BaseDTO) for item in value):
                    # Convert list of DTOs to list of dictionaries
                    result[api_field_name] = [item.to_dict() for item in value]
                elif value and all(isinstance(item, datetime) for item in value):
                    # Convert list of datetimes to list of ISO format strings
                    result[api_field_name] = [item.isoformat() for item in value]
                else:
                    # Keep other lists as is, assuming they are serializable
                    result[api_field_name] = value
            elif isinstance(value, dict):
                # Process dictionary values recursively
                processed_dict = {}
                for k, v in value.items():
                    if isinstance(v, datetime):
                        processed_dict[k] = v.isoformat()
                    elif isinstance(v, BaseDTO):
                        processed_dict[k] = v.to_dict()
                    elif hasattr(v, '__dict__'):
                        # Handle objects with __dict__ that aren't BaseDTO
                        processed_dict[k] = vars(v)
                    else:
                        processed_dict[k] = v
                result[api_field_name] = processed_dict
            elif hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool)):
                # Handle custom objects that aren't BaseDTO by using vars()
                result[api_field_name] = vars(value)
            elif isinstance(value, (str, int, float, bool)) or value is None:
                # Keep primitive types as is
                result[api_field_name] = value
            else:
                # Try to convert to string as a last resort
                try:
                    result[api_field_name] = str(value)
                except:
                    raise ValueError(f"Value for field '{field_name}' is not JSON serializable: {value}")
            
        return result
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create a DTO from a dictionary (typically from API response).
        
        Args:
            data: Dictionary from API response
            
        Returns:
            An instance of the DTO class
        """
        # Reverse the field mapping
        reverse_mapping = {v: k for k, v in cls._api_field_mapping.items()}
        
        # Apply field mappings
        kwargs = {}
        for field_name, value in data.items():
            # Get the Python field name or use the API field name if no mapping exists
            py_field_name = reverse_mapping.get(field_name, field_name)
            kwargs[py_field_name] = value
            
        return cls(**kwargs)
    
    def to_json(self) -> str:
        """
        Convert the DTO to JSON.
        
        Returns:
            str: JSON representation of the DTO
        """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """
        Create a DTO from a JSON string.
        
        Args:
            json_str: JSON string
            
        Returns:
            An instance of the DTO class
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        Convert camelCase to snake_case.
        
        Args:
            name: camelCase string
            
        Returns:
            str: snake_case string
        """
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    @staticmethod
    def snake_to_camel(name: str) -> str:
        """
        Convert snake_case to camelCase.
        
        Args:
            name: snake_case string
            
        Returns:
            str: camelCase string
        """
        components = name.split('_')
        return components[0] + ''.join(x.title() for x in components[1:]) 