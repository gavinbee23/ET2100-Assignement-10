from dataclasses import dataclass


@dataclass(frozen=True)
class NPC:
    name: str
    role: str
    dialogue: str


NPCS = {
    "m": NPC("Mara Venn", "radio dispatcher",
             "The emergency broadcast is coming from below the hospital. Take my badge."),
    "o": NPC("Oren Pike", "quartermaster",
             "I take gold. Paper won't last another minute in this rain."),
    "i": NPC("Inez Calder", "trauma nurse",
             "I left a sealed case in the far ward. Bring it here and I'll split the supplies."),
    "t": NPC("Tavi Rowe", "trapped courier",
             "That thing kept pacing outside the door. Can you clear the hall for me?"),
    "l": NPC("Lin Sato", "pump engineer",
             "I can lift the service hatch with the ward's relay. The pumps below are still running."),
}
