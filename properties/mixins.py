
class CommonPropertiesMixin():
    
    @property
    def cat_key(self):
        return self.property.property_category.cat_key
