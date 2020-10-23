
_key_dict = {
    "kosis": ["YOUR_APIKEY"]
}

_gen_dict = {}


def create_generator(name):
    auth_data = _key_dict[name]
    end_idx = len(auth_data)
    curr_idx = -1
    while True:
        curr_idx += 1
        if(curr_idx >= end_idx):
            curr_idx = 0
        yield auth_data[curr_idx]

def get_key(name):
    if name not in _gen_dict:
        _gen_dict[name] = create_generator(name)
    return next(_gen_dict[name])
