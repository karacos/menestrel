
import karacos

class EntriesHolder(karacos.db['WebNode']):
    """
    Container type for Entries
    """
    
    def _entry_publish(self,entry):
        """
        Triggered action by Entries when published
        """
        assert False, "Please implement this method in subclasses"
    
    @karacos._db.isaction
    def subscribe(self):
        pass