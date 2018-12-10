def get_default_channel_configs(num_channels):
    return {
        'board_mode': 'default',
        'sample_rate': 250,
        'channels': [
            {
                'enabled': True,
                'parameters': {
                    'power_down': 'OFF',
                    'gain': 24, 'input_type': 'NORMAL',
                    'bias': 1, 'srb2': 1, 'srb1': 0,
                },
            }
        ] * num_channels
    }
