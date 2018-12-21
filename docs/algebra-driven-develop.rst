Algebra-driven development
==========================

I like to call it "algebra driven development" and by algebra I mean a (mathematical) set of values and a set of operators that act on
those values.

https://en.wikipedia.org/wiki/Algebra#cite_note-2

Mathematical algebras
---------------------

Some examples from mathematics are:

* 8-bit unsigned integers (0 to 255)
* 8-bit signed integers (-128 to 127)
* the integers in the abstract (ℤ)
* rational numbers (ℚ)
* the "real" numbers in the abstract (ℝ)
* 80-bit precision floating point numbers
* "BigDecimal" in Java
* Complex numbers (ℂ)
* Single and multiple-dimensional arrays such as those implemented in ``numpy``

Operators that make sense on those things are addition,  subtraction,  multiplication,  equality testing,  etc.  The numbers in
that list are substituitable for each other to some extent.  For instance if you want to count from 0 to 100 (or reason about that process)
all of the above are good,  particularly those 8-bit unsigned.  If you need to count to 150,  however,  those break down.

Here we see a contradiction between idealist and materialist perspectives.  

One philosopher (an idealist) might say that the integers (ℤ) are "real" because they exist in the abstract and we can write proofs about them,
they don't have the arbitrary restrictions that (say) the 8-bit integers have.

Another philosopher (a materialist) might say that the 8-bit integers are "real" because they are realized on the computers we use.

This is essential to software engineering:  computers are physical machines that operate on things that we think about.  We always
are going to have things that exist in our mind (mathematical concepts,  how the customer thinks about their business,  what the end user
is supposed to believe above the system) and a physical manifestation of those things.  Going from "somebody wants X" to working software
means creating (whether we know we are or not) models of the system at increasingly detailed levels

https://en.wikipedia.org/wiki/Refinement_(computing)

until one of those "models" is the product.

