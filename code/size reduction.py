  # still need the size reduction
    # size reduce by alg3 which is the Hermite one
	def size_reduce(b, b1, mu):
	#Adjusts b to be size-reduced w.r.t b1 (i.e., mu is between -0.5 and 0.5).
		k = np.round(mu)
		b_reduced = b - k * b1
		# Recalculate new mu (should be between -0.5 and 0.5)
		mu_reduced = mu - k
		return b_reduced, mu_reduced

# the basic swap necessary
