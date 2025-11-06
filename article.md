# Overview

## How serious are quantum computers?

The question of quantum computing has been discussed from many angles. Some argue the ’fear’ of a post-quantum world is not needed, due to the vanishing likelihood of a quantum computer being capable of functioning [37]. Others have argued that AI and Quantum-Cryptography should be used in conjunction to solve large, complex problems with the use of AI algorithms secured with unbreakable cryptography, for cryptoanalysis, understanding better optimisations and providing more accurate answers [36]. These are yet to be proved [36]. In fact, at the point of writing, new standards in PQC have not even been out for a whole year, and many are still being developed. 

Authors in the past have worked on several different types of post-quantum encryption schemes, only to see them fail security tests set aside by some of the largest cryptography organisations in the world [35], such as BIKE, NTRU, and others. The selection of PQC algorithms are informed by a National Institute of Standards and Technology (NIST) process. In doing so, candidate PQC algorithms are evaluated and scrutinised in successive rounds to ensure they will meet requirements to protect sensitive or classified data. In fact, it was only as early as 2024 August that the first three were identified after numerous trials of other competing algorithms globally, to find the most secure post-quantum ones [30, 31, 33, 29].  

The U.S. National Institute of Standards and Technology (NIST) has released several new Federal Information Processing Standards (FIPS) that are based on lattice cryptography, marking a significant step toward a quantum-resistant cryptographic infrastructure.

### State of the ART PQC Algorithms

These three standards are the first of their kind, selected by NIST after a multi-year competition to find algorithms resistant to quantum attacks. While FIPS 205 uses a hash-based approach, FIPS 203 and FIPS 204 are built on lattice-based cryptography.

### FIPS-203

This is a Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM). This standard is based on the CRYSTALS-Kyber algorithm [33, 34, 30, 31]. It’s designed for key establishment or key exchange, which is a fundamental part of secure communication (like TLS). Instead of directly encrypting data, ML-KEM is used to securely exchange a shared secret key between two parties [33, 34, 30, 31]. This shared key can then safely be used for symmetric encryption, which as previously discussed is already considered quantum-resistant with a sufficiently large key size.

### FIPS 204

This is a Module-Lattice-Based Digital Signature Algorithm (ML-DSA) [33, 34, 30]. This standard uses the CRYSTALS-Dilithium algorithm [33, 34, 30]. It’s a digital signature scheme, meaning it’s used to verify the authenticity and integrity of data, like a document or a software update [33, 34, 30]. ML-DSA provides a quantum-safe replacement for current digital signature algorithms like RSA and ECC [33, 34, 30].

### FIPS 205

This is based on a Stateless Hash-Based Digital Signature Standard (SLH-DSA) [33, 34, 30, 31]. This standard is specifically used for the alternative
to the current digital signature scheme [33, 34, 30, 31]. While not lattice-based, it’s also designed to be quantum-resistant. It uses cryptographic hash functions to provide security [33, 34, 30]. Cryptographic hash functions are another type of functions that are thought to be quantum-resistant. In summary, FIPS 203 and FIPS 204 use lattice-based cryptography to address the two primary functions of public-key cryptography: secure key exchange and digital signatures. Together with FIPS 205, they provide the world with a new set of standards for organisations to begin their transition to a quantum-safe future [33, 34, 30]. And, although this is useful, it is doubtful these will be adopted by all and sundry within the next few years.

## Potential Future in PQC

### Protecting against ”Harvest Now, Decrypt Later” Threat

A key driver for immediate action is the concept of ”harvest now, decrypt later.” This is a popular approach because of the future gain associated with the product - sensitive encrypted data [33, 34, 30, 35, 29]. Malicious actors, including nation-states, are already stockpiling vast amounts of encrypted data that they cannot currently decrypt. The goal being, once they are able to access a sufficiently powerful quantum computer, they can decrypt all this sensitive data, which would inevitably lead to one of the largest data breaches globally. Therefore, protecting against this is imperative with early adoption.

## The Challenges of Transitioning to PQC

There is a lack of cryptographic flexibility holding back organisations: many companies lack a detailed inventory of their cryptographic assets and a clear understanding of where and how encryption is used, or are not able to transition to a more complicated, quantum-encryption scheme [23]. There is also a challenge to early adopters, as they must also be backwards compatible, if they are using post-quantum encryption schemes. We know from network protocols that both the client and server have to agree on a communication methodology, and if only one side is using PQC, then the other side must fall-back to the version they have in common - the chain only being ”as strong as the weakest link”, there is no benefit for early adopters as they carry all the financial and technical burden but will have to wait some time to see the benefit. Adoption may be computationally more expensive: The new NIST-standardised PQC algorithms, such as lattice-based cryptography, have different performance characteristics (e.g., larger key sizes, slower speeds) that may require significant re-engineering of existing systems and protocols [33, 34].

### The Potential Solution: Role of Hybrid Quantum - Classical Algorithms

While the focus is on a full migration to PQC, hybrid quantum-classical algorithms are emerging as a crucial stepping stone and a long-term solution. These algorithms, which combine the strengths of both classical and quantum computers, are particularly relevant in the ”Noisy Intermediate-Scale Quantum” (NISQ) era [33, 34, 22], where quantum-computers have yet to achieve their peak potential, largely because of all the noisy errors they are generating [22]. Hybrid algorithms use some components of lattice-based cryptography or other areas of mathematics like the previously named hash functions) for use in their functions, which allows companies, organisations and peak bodies make half the transition necessary to fully post-quantum encryption algorithms [22, 33]. 

This is considered computationally much less expensive, more practical, and easier for companies and governments to start working towards now.  Also, the benefits from doing this are likely to bring longer decryption times to any data stored away from harvesting, so is a practical measure that can be taken almost immediately [34, 22, 35].
