import numpy as np
from logger import log
from array_grid import get_next_grid_dims
from act_on_image import ActOnImage
from array_message import write_conjugated_message_grids
from bpcs_steg import arr_bpcs_complexity

def remove_message_from_vessel(arr, alpha, grid_size):
    messages = []
    nfound, nkept, nleft = 0, 0, 0
    for dims in get_next_grid_dims(arr, grid_size):
        nfound += 1
        grid = arr[dims]
        if arr_bpcs_complexity(grid) < alpha:
            nleft += 1
            continue
        nkept += 1
        messages.append(grid)
    assert nfound == nkept + nleft
    log.critical('Found {0} out of {1} grids with complexity above {2}'.format(nkept, nfound, alpha))
    return messages

class BPCSDecodeImage(ActOnImage):
    def modify(self, alpha):
        return remove_message_from_vessel(self.arr, alpha, (8,8))

def bpcs_steg_decode(infile, outfile, alpha):
    x = BPCSDecodeImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    grids = x.modify(alpha)
    write_conjugated_message_grids(outfile, grids, alpha)

def test_decode_1():
    from bpcs_steg import max_bpcs_complexity
    alpha = 40.0/max_bpcs_complexity(8,8)
    infile = 'docs/secretary-general.bmp'
    outfile = 'docs/secretary-general.txt'
    bpcs_steg_decode(infile, outfile, alpha)

def decode_vessel():
    infile = 'docs/vessel_encoded.png'
    outfile = 'docs/vessel_message.txt'
    alpha = 0.45
    bpcs_steg_decode(infile, outfile, alpha)

def decode_mini_vessel():
    infile = 'docs/vessel_mini_encoded.png'
    outfile = 'docs/vessel_mini_message.txt'
    alpha = 0.45
    bpcs_steg_decode(infile, outfile, alpha)

if __name__ == '__main__':
    decode_mini_vessel()