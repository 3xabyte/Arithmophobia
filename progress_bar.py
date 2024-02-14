class ProgressBar:
    """
    -----------------------------------------------------------------------
    A progress bar class which uses characters to visualize everything.
    -----------------------------------------------------------------------
    Author:     Matt McBurnie
    Version:    1.0a
    Updated:    2024/02/12
    -----------------------------------------------------------------------
    """

    def __init__(self, right, total, count=50, correct_bar='🟩', wrong_bar='⬛'):
        """
        -----------------------------------------------------------------------
        Initializes a progress bar.
        Use: p = ProgressBar(right, total, count*, correct_bar*, wrong_bar*)
        * Denotes optional parameter
        -----------------------------------------------------------------------
        Parameters
        right → int: The current value for the progress bar. Used as a
        numerator.
        total → int: The maximum value for the progress bar. Used as a 
        denominator.
        count → int (Default = 50): A count for how big the progress bar should
        be.
        correct_bar → str(1) (Default = '🟩'): The character to use for the 
        'progress' part of the progress bar.
        wrong_bar → str(1) (Default = '⬛'): The character to use to show the 
        'background' of the progress bar. 
        -----------------------------------------------------------------------
        
        """
        
        if(right > total):
            raise Exception("Progress bar can not go above 100%.")
        
        self._right = right
        self._total = total
        self._count = count
        self._correct_bar = correct_bar
        self._wrong_bar = wrong_bar

        return
    
    def __str__(self):
        
        correct_bars = 0

        # 100%
        if(self._right == self._total):
            correct_bars = self._count
        # 0%
        elif(self._right == 0):
            pass
        else:

            i = 1
            while(i < self._count and ((i / self._count) <= (self._right / self._total))):
                correct_bars += 1
                i += 1

        wrong_bars = self._count - correct_bars

        output = "{:}{:}".format(self._correct_bar * correct_bars, self._wrong_bar * wrong_bars)
        
        return output
    
    def progress(self):
        if(self._right < self._total):
            self._right += 1
        return
    
