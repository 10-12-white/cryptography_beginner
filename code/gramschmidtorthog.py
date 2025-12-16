    # need to gram schmidt so that we can go from this to integer points back to the same lattice
    # vectors in the basis for b, b1 are swapped and labelled
	def gram_schmidt_projection(b, b1):
	#Actions: computes the projection of vector b onto the orthogonal complement of b1.
	#Returns: b_prime (the projection) and mu (the coefficient).
		if np.linalg.norm(b1) == 0:
			return b, 0
    # mu_21: coefficient for b2 projection onto b1
		mu = np.dot(b, b1) / np.dot(b1, b1)
		b_prime = b - mu * b1
		print("The shortest vector is", b_prime)
    print("the GSO coeff is ", mu )
    return b_prime, mu
# vector_basis = (vector[1,2,3],vector[4,5,6])
# shortened_basis = gram_schmidt_projection(vector[1,2,3],vector[4,5,6])
