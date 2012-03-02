from rv import rvtypes, commands

class AudioForSequence(rvtypes.MinorMode):
    """Simplify adding of audio to a sequence of images."""

    def add_audio(self, event):
        """Ask the user for a file and add it as audio to the currently selected sequences."""
        # The idea here is to use RVs stack to create two "tracks". The first input will be a
        # sequence of all the current sources, and the second the selected audio file.
        selected_files = commands.openMediaFileDialog(False, commands.OneExistingFile, "", "", "")

        # Create a new source for the selected file. We'll do this here to fail early
        # and not leave junk nodes laying around.
        audio_source = commands.addSourceVerbose([selected_files[0]], "")
        audio_group = commands.nodeGroup(audio_source)

        # Create a new sequence. We're assuming here that the current sequence is the default
        # sequence, which always contains all sources known to RV. We'll need our own copy since
        # we want to keep the audio out of our "video track".
        sequence = commands.newNode("RVSequenceGroup", "SequenceForAudioStack")

        # Find all the sources connected to the current sequence, and connect them to the new one.
        current_sources = []
        current_sequence = commands.viewNode()
        inputs, _ = commands.nodeConnections(current_sequence, False)
        for node in inputs:
            if commands.nodeType(node) == "RVSourceGroup":
                current_sources.append(node)
        commands.setNodeInputs(sequence, current_sources)

        # Create the stack and connect the two sources.
        stack = commands.newNode("RVStackGroup", "StackWithAudio")
        commands.setNodeInputs(stack, [sequence, audio_group])

        # Find the actual stack node and configure it to to use the topmost 
        # source (no compositing) and only the audio we just loaded. This should mean
        # that if the user selects a file containing both audio and video as the audio
        # source, they will still get the expected result.
        for node in commands.nodesInGroup(stack):
            if commands.nodeType(node) == "RVStack":
                commands.setStringProperty("%s.composite.type" % (node), ["topmost"], False)
                commands.setStringProperty("%s.output.chosenAudioInput" % (node), [audio_group], False)
                break

        commands.setViewNode(stack)

    def menu_state_add_audio(self):
        """Return current state of the 'Add Audio to Sequence' menu item."""
        # If the user is currently viewing a sequence with any inputs, enable the menu item.
        current_view = commands.viewNode()
        if commands.nodeType(current_view) == "RVSequenceGroup":
            inputs, _ = commands.nodeConnections(current_view, True)
            if inputs:
                return commands.NeutralMenuState
        return commands.DisabledMenuState

    def __init__(self):
        rvtypes.MinorMode.__init__(self)
        self.init("audioforsequence-mode", 
                  None,
                  None,
                  [ ("Audio", 
                    [ ("Add Audio to Sequence", self.add_audio, "", self.menu_state_add_audio) ])
                  ])


def createMode():
    """Required to initialize the module. RV will call this function to create your mode."""
    return AudioForSequence()
