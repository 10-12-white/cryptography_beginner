# edit to fplll is the backend and super fast
from fpylll import LLL, BKZ, IntegerMatrix, GSO, SVP

# dual_block_reduc done by Micciancio & Walter's Self-Dual BKZ
# will return a basis that is dual-reduced for that block
def dual_block_reduction(basis, block_start, block_size):
    # gso
    gso = GSO.Mat(basis)
    gso.update_gso()
    
    # 2. Extract the local block we want to reduce in the dual
    # We find a short vector in the dual of the projected block.
    # This vector corresponds to a 'large gap' in the primal.
    
    # 3. Apply a Dual-SVP solver
    # fpylll's BKZ.Reduction does this internally if 'flags=BKZ.DUAL_REDUCTION'
    # In practice, self-dual BKZ uses a 'wrapper' that treats the 
    # reversed dual GSO as a primal GSO to save computation, because there is less work to do on the GSO, 
    # than to create A = B^-1 * t
    params = BKZ.Param(block_size=block_size, strategies=BKZ.DEFAULT_STRATEGY, 
                       flags=BKZ.DUAL_REDUCTION)
    
    BKZ.Reduction(gso, LLL.Wrapper(gso), params)()

    # return for the next component in the program
    return basis
