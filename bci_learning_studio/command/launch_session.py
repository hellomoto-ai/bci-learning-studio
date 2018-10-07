import argparse

import bci_learning_studio.session


def _parse_args(args, sessions):
    parser = argparse.ArgumentParser(
        description='Launch an interactive session.'
    )
    parser.add_argument(
        'session', choices=sessions,
    )
    namespace, args = parser.parse_known_args(args)
    return namespace, args


def main(args):
    """Entrypoint for `launch_session` command"""
    sessions = {
        module: getattr(bci_learning_studio.session, module)
        for module in bci_learning_studio.session.__all__
    }
    namespace, args = _parse_args(args, sessions)
    sessions[namespace.session](args)
