from typing import Any
from flet import Audio
from flet_core.audio import ReleaseMode
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from Source import WARNING_MUSIC

class AudioPlayer(Audio):
    def __init__(self, 
                 src = WARNING_MUSIC,
                 ref: Ref | None = None, 
                 data: Any = None, 
                 src_base64: str | None = None,
                 autoplay = False, 
                 volume = 1, 
                 balance = 0,
                 playback_rate: OptionalNumber = None,
                 release_mode: ReleaseMode | None = None, 
                 on_loaded=None, 
                 on_duration_changed=None, 
                 on_state_changed=None, 
                 on_position_changed=None, 
                 on_seek_complete=None
                 ):
        super().__init__(
            src, 
            ref,
            data, 
            src_base64, 
            autoplay,
            volume, 
            balance,
            playback_rate, 
            release_mode, 
            on_loaded, 
            on_duration_changed, 
            on_state_changed, 
            on_position_changed, 
            on_seek_complete
            )
        