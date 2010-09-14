
import KaraCos

class EntriesHolder(KaraCos.Db.WebNode):
    """
    Container type for Entries
    """
    
    def _entry_publish(self,entry):
        """
        Triggered action by Entries when published
        """
        assert False, "Please implement this method in subclasses"