"""
WhiskerNotes - Validation Utilities
Input validation for notes
"""

from utils.exceptions import ValidationError


class NoteValidator:
    """Validator for note data"""
    
    MAX_TITLE_LENGTH = 200
    MAX_CONTENT_LENGTH = 100000
    VALID_CATEGORIES = ["Personal", "Study", "Ideas", "Work", "Other"]
    
    def validate_title(self, title: str) -> None:
        """
        Validate note title
        
        Args:
            title: Title to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(title, str):
            raise ValidationError("Title must be a string")
        
        title = title.strip()
        
        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValidationError(f"Title must be less than {self.MAX_TITLE_LENGTH} characters")
    
    def validate_content(self, content: str) -> None:
        """
        Validate note content
        
        Args:
            content: Content to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(content, str):
            raise ValidationError("Content must be a string")
        
        if len(content) > self.MAX_CONTENT_LENGTH:
            raise ValidationError(f"Content must be less than {self.MAX_CONTENT_LENGTH} characters")
    
    def validate_category(self, category: str) -> None:
        """
        Validate note category
        
        Args:
            category: Category to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(category, str):
            raise ValidationError("Category must be a string")
        
        # Remove emoji if present
        category_clean = category.split()[0] if ' ' in category else category
        
        if category_clean not in self.VALID_CATEGORIES:
            raise ValidationError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")
    
    def validate_tags(self, tags: str) -> None:
        """
        Validate note tags
        
        Args:
            tags: Tags to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(tags, str):
            raise ValidationError("Tags must be a string")
        
        # Tags are optional, so empty string is valid
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            if len(tag_list) > 20:
                raise ValidationError("Maximum 20 tags allowed")
            
            for tag in tag_list:
                if len(tag) > 30:
                    raise ValidationError("Each tag must be less than 30 characters")

