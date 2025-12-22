"""
This is normal BKZ:
For a lattice basis L and a block size k:
    Preprocessing: Run LLL on the entire basis to get it into a decent starting shape.
    The Outer Loop (Tours): Repeat the following until the basis stabilizes:
        The Inner Loop (Sliding Window): For i=1 to n−1:
            Define the current block size h=min(k,n−i+1).
            Local Projection: Project the vectors bi​,…,bi+h−1​ onto the space orthogonal to b1​,…,bi−1​. (This focuses the algorithm only on the "new" information in that block).
            SVP Oracle: Find the absolute shortest vector (v) in this small h-dimensional projected lattice. This is the "expensive" part where we use enumeration or sieving.
            Update: If this new vector v is shorter than the current bi​, insert it into the basis.
            Local LLL: Because you just added a vector, the basis is now "linearly dependent" (too many vectors). Run LLL on this local block to remove the dependency and clean up the vectors.

DYNANIC BKZ is slightly different:
"""

