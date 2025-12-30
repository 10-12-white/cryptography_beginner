
# Project Motivation

The focus of this work is via https://arxiv.org/pdf/2311.15064#cite.micciancioPracticalPredictableLattice2016

This paper, the main motivation for this project, introduces a recursive lattice reduction framework designed to solve two core problems in lattice theory: finding the shortest non-zero vector (SVP) and locating dense sublattices within a larger lattice. The central idea is to try and break down the larger problem on a high-rank lattice into simpler, lower-rank subproblems. This is achieved through an iterative process of finding dense sublattices within dense sublattices (or their duals), where the rank progressively decreases at each step.  This method provides an elegant and effective approach to handle the task of fidning solutions within these higher ranked lattices.

There are a few reaons this is helpful.  One, it is similar to BKZ and LLL, in that it is overall reducing the size of the lattice in solving.  And two, it it is shown to be an efficient reduction that matches the effective trade-off achieved by the best existing basis reduction algorithms available today.

The formal algorithm, A(L,aux), demonstrates how this recursion works in practice, by reducing the γ-HSVP problem on an n-rank lattice to the δk​​-HSVP on a smaller k-rank lattice. For lattices that are still large, the framework is instructed to find a sublattice L′ with a lower rank and a small determinant, and then recursively call the function on that new sublattice. The entire process is managed by auxiliary information (aux), which is vital for both tracking the sublattice rank and controlling the overall computational running time to ensure efficiency.

Crucially, the recursion must terminate. When the algorithm reaches a lattice (L) with a sufficiently small rank (n≈k), the framework switches from the recursive search to an optimized, known algorithm (acting as an oracle) to find the shortest vector efficiently. By balancing the depth of the recursive search with the final, high-performance base-case solver, the proposed recursive framework achieves a significant result: 

This is the motivation.  How can we use this information about sublattices to improve the efficiency of BKZ, or another sorting algorithm, that helps reduce the overall size of the basis vectors.  And in fact, the apper poses many open questions.  Such as, is there a way of making them comparable?  How efficient is this algorithm in comparison to BKZ, LLL? Does it do a similar job?  The code for the project is prpvided in their GitHub, available here: {PROVIDE_LINK}.  But, the authord acknowledge that efficiencies within the code was not their first priority - can we make it faster? If so, how?

## Project Gaols

- Make a list of links between lattice reduction reduction (yes its said like that) to LLL
- Reduce complexity of the programming style reviewed in this paper
- Understand the maths in it
- Write up LLL
- Write up BKZ
- focus on lattice-reductin-reductions
- Present
- finish up the chaoter


## Contributions

In this repo, there is code for LLL. Have a play, see if you can make it faster.  Values have already been tested to ensure it is performing like SageMaths baked in biscuit-tin LLL, which is great.  We have not yet done the same with BKZ, this is the next step.  The maths for it has been understood, and its been written up in an Overleaf.  Will be getting to sharing it in due time.  For now, working on the way that we see the next stage of our progress going...

### References

7] Jean-Philippe Aumasson, Serious Cryptography, 2nd Edition, ”A Practical Introduction to Modern Encryption” August 2024, ISBN-13: 9781718503847 

[8] Algorithms for the Closest and Shortest Vector Problems, Mathematics of University of Auckland, https://www.math.auckland.ac.nz/ sgal018/crypto-book/ch18.pdf

[9] Advanced Topics in Cryptography: Lattices, Vinod Vaikuntanathan, Computational Problems, Online, Available: https://people.csail.mit.edu/vinodv/6876-Fall2015/L3.pdf

[10] University of San Diego, CSE 206A: Lattice Algorithms and Applications, Daniele Micciancio, https://cseweb.ucsd.edu/classes/wi12/cse206A-a/lec3.pd

[22] Wikipedia, Noisy intermediate-scale quantum era, 2024 https://en.wikipedia.org/wiki/Noisy intermediate-scale quantum era

[23] The anticipated arrival of quantum computers poses significant cybersecurity risks for those who do not prepare early, 2025, https://www.actuaries.asn.au/research-analysis/c-suite-should-be-concerned-about-post-quantum-cryptography

[24] IQM and VTT Launch Europe’s 1st 50-Qubit Superconducting Quantum Computer, March 4, 2025 https://www.hpcwire.com/off-the-wire/iqm-and-vtt-launch-europes-1st-50-qubit-superconducting-quantum-computer/

[25] Doerr and Levasseur ”Applied Discrete Structures” https://math.libretexts.org/Applied Discrete Structures (Doerr and Levasseur)/16%3A An In

[26] UCLA, ”Circles” https://circles.math.ucla.edu/circles/lib/data/Handout-3861-3432.pdf

[27] UCI, Graduate Algebra, Midterm Practise Problems, https://www.math.uci.edu/˜nckaplan/teaching files/graduate algebra/Math206B Midterm2 P

[28] Wikipedia, Lattice Groups, [Online], Available: https://en.wikipedia.org/wiki/Lattice (group)

[29] Planning for post-quantum cryptography, [Online], Available: https://www.cyber.gov.au/resources-business-and-government/governance-and-user-education governance/planning-post-quantum-cryptography

[30] Post-Quantum Cryptography Initiative , [Online], Available: https://www.cisa.gov/resources-tools/resources/quantum-readiness-migration-post-quantum-cryptography

[31] NIST, ”Why prepare Now? Quantum Readiness”, 2023, [Online], Available: https://www.cisa.gov/sites/default/files/2023-08/Quantum

[32] Chris Vale, Shor and Grover’s algorothms, [Online], Available: https://kuscholarworks.ku.edu/server/api/core/bitstreams/0b163bff-f673-454e-b0e4-8a2e4abc7b9a/content

[33] NIST, Announcing Approval of Three Federal Information Processing Standards (FIPS) for Post-Quantum Cryptography , [Online], Available: https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved

[34] NIST, Finalising An Important Step Towards Quantum Safe Future, [Online], Available: https://cloudsecurityalliance.org/blog/2024/08/15/nist-fips-203-204- and-205-finalized-an-important-step-towards-a-quantum-safe-future

[35] Nilsson, A. (2023). Decryption Failure Attacks on Post-Quantum Cryptography. [Doctoral Thesis (compilation), Department of Electrical and Information Technology]. Lunds Universitet, [Online], Available: https://lup.lub.lu.se/search/files/143742917/thesis.pdf


