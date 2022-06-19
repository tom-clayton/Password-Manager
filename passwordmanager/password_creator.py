
from random import choice

class PasswordCreator(object):
    """Creates a random password.""" 
    lower_chars = list(range(97, 123))
    upper_chars = list(range(65, 91))
    digits = list(range(48,57))
    special_chars = [33] + list(range(35, 48)) + list(range(60, 65))\
                    + list(range(91, 97))
        
    def create(self, length, uppercase, digits, special):
        """Create password from pool.
        Check password has at least one character from each selected
        category.

        Attributes:
        length - length of password
        uppercase - include uppercase characters
        digits - include digits
        special - include special characters
        """

        pool = []
        pool += self.lower_chars
        if uppercase:
            pool += self.upper_chars
        if digits:
            pool += self.digits
        if special:
            pool += self.special_chars
        
        valid_password = False
        while not valid_password:
            password = ""
            lowercase_included = False
            uppercase_included = False
            digit_included = False
            special_included = False

            for i in range(length):
                char = choice(pool)
                if char in self.lower_chars:
                    lowercase_included = True
                elif char in self.upper_chars:
                    uppercase_included = True
                elif char in self.digits:
                    digit_included = True
                elif char in self.special_chars:
                    special_included = True
                password += chr(char)

            if  (lowercase_included) \
                and (not uppercase or uppercase_included) \
                and (not digits or digit_included) \
                and (not special or special_included):
                valid_password = True
                
        return password
