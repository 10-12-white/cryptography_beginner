# built in SgaeMaths technique 
# Define a matrix representing a lattice basis (rows are vectors)
M = matrix(ZZ, [[1,1], [1,100]])

# Get the LLL-reduced basis
reduced_basis = M.LLL()
print("My reduced basis is ")
print(reduced_basis)
