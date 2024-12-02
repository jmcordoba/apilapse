class PeriodicityValidator:
    """
    Class responsible for validating the periodicity parameter.
    """
    @staticmethod
    def is_valid_periodicity(periodicity):
        """
        Validate that the periodicity is one of the allowed values: 'hourly', 'daily', or 'weekly'.
        
        :param periodicity: The periodicity to validate.
        :return: True if the periodicity is valid, False otherwise.
        """
        allowed_values = ['hourly', 'daily', 'weekly']
        return periodicity in allowed_values
