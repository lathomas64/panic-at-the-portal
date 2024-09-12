'''
module defining Amplify Action
'''
from prototype.actions.action import Action

class AmplifyAction(Action):
    '''
    Amplify action
    3+ Amplify
    Your next Action this turn has its range increased by 2 and can apply to 3 extra targets.
    '''

    def confirm_targets(self, actor, die, _target_hex):
        raise NotImplementedError("next action +2 range +3 targets")
