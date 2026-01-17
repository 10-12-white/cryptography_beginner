
# Project Motivation

The focus of this work is via https://arxiv.org/pdf/2311.15064#cite.micciancioPracticalPredictableLattice2016

This paper, the main motivation for this project, introduces a recursive lattice reduction framework designed to solve two core problems in lattice theory: finding the shortest non-zero vector (SVP) and locating dense sublattices within a larger lattice. The central idea is to try and break down the larger problem on a high-rank lattice into simpler, lower-rank subproblems. This is achieved through an iterative process of finding dense sublattices within dense sublattices (or their duals), where the rank progressively decreases at each step.  This method provides an elegant and effective approach to handle the task of fidning solutions within these higher ranked lattices.

There are a few reaons this is helpful.  One, it is similar to BKZ and LLL, in that it is overall reducing the size of the lattice in solving.  And two, it it is shown to be an efficient reduction that matches the effective trade-off achieved by the best existing basis reduction algorithms available today.

The formal algorithm, A(L,aux), demonstrates how this recursion works in practice, by reducing the γ-HSVP problem on an n-rank lattice to the δk​​-HSVP on a smaller k-rank lattice. For lattices that are still large, the framework is instructed to find a sublattice L′ with a lower rank and a small determinant, and then recursively call the function on that new sublattice. The entire process is managed by auxiliary information (aux), which is vital for both tracking the sublattice rank and controlling the overall computational running time to ensure efficiency.

Crucially, the recursion must terminate. When the algorithm reaches a lattice (L) with a sufficiently small rank (n≈k), the framework switches from the recursive search to an optimized, known algorithm (acting as an oracle) to find the shortest vector efficiently. By balancing the depth of the recursive search with the final, high-performance base-case solver, the proposed recursive framework achieves a significant result: 

This is the motivation.  How can we use this information about sublattices to improve the efficiency of BKZ, or another sorting algorithm, that helps reduce the overall size of the basis vectors.  And in fact, the apper poses many open questions.  Such as, is there a way of making them comparable?  How efficient is this algorithm in comparison to BKZ, LLL? Does it do a similar job?  The code for the project is prpvided in their GitHub, available here: {PROVIDE_LINK}.  But, the authord acknowledge that efficiencies within the code was not their first priority - can we make it faster? If so, how?

## Project Goals

- Make a list of links between lattice reduction reduction (yes its said like that) to LLL
- Reduce complexity of the programming style reviewed in this paper
- Understand the maths in it
- Write up LLL
- Write up BKZ
- focus on lattice-reductin-reductions
- Present
- finish up the chaoter

### Done

- chapter down to 23 pages
- AMSI presentation slides nearly done
- written backlog up
- worked on review
- review on the slides
- review on the chapter
- awaiting inspiration for the next moves made
- writeup bk2 2.0
- write up dual-bkz 2.0
- awaiting supervisor review for chapter  
- waiting for supervisor review on AMSI presentation first
- awaing for changes on next slides

### Left to do Jan

- edit code for dual-intuitive bkz 2.0
- work on the maths behind enum in SVP
- message AMSI for supervisors on project
- how can we measure wastage in the SVP solver for BKZ2.0
- What is reduction in efforts as opposed to using Dual-Intuitive BKZ (DIBKZ)
- Find good example lattice basis to construct within?
- Introduce the SVP challenge to your supervisors
- Work on trying to explain basic properties first
- Read the edits, and then work on them so that you are getting better at it
- practise presenting

### Left to do Feb

- present
- practise present

### The shape of the different options:

| Algorithm,|        Primary Advantage,     | When to use for Research  |
| BKZ 2.0,   |       Pruning & Heuristics,  | The standard baseline for most papers. |
| Progressive BKZ,|  Speed of Convergence,  | When you want to show your algorithm is "fast." |
| Sieve-BKZ (G6K), | Massive Blocksizes,    | When testing against very high-dim challenges.  |
| Self-Dual BKZ,   | GSA Consistency,       | When you want the most "accurate" GSO profile.  |

## Contributions

In this repo, there is code for LLL. Have a play, see if you can make it faster.  Values have already been tested to ensure it is performing like SageMaths baked in biscuit-tin LLL, which is great.  We have not yet done the same with BKZ, this is the next step.  The maths for it has been understood, and its been written up in an Overleaf.  Will be getting to sharing it in due time.  For now, working on the way that we see the next stage of our progress going...




