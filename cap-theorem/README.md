# CAP Theorem — Partition Park

Not a text curriculum like the Kubernetes course — this one's a low-poly,
interactive simulation. **Open [`index.html`](./index.html) in a browser.**
Everything below is the accurate explanation behind what you're looking at,
sourced directly from the primary papers (not blog-post summaries of them).

## What you're controlling

Three replica nodes sit around a client, connected by tracks that carts
(requests) ride back and forth on. You can:

- **Pause/resume the flow** at any time.
- **Cut off a node** — this opens a gap in its track. This is the only way
  a partition happens in the simulation, deliberately: it's something that
  happens *to one node*, not a global switch flipped over the whole system.
- While a node is cut off, **choose what happens to requests that reach the
  gap**: wait for the node to come back (consistent, not available), or
  answer immediately from local, possibly-stale data (available, not
  guaranteed consistent). You can change your mind mid-partition — already
  answered requests stay whatever they were, only new arrivals follow the
  new choice.
- **Heal** the node — this runs a visible reconciliation pass, not an
  instant fix.

## Why it's built this way (the corrected version of CAP theorem)

The popular one-liner — "a distributed system can only have 2 of
Consistency, Availability, and Partition tolerance" — is the version even
the theorem's own author has disavowed. Here's what's actually true, with
sources:

1. **Partition tolerance isn't a toggle.** In a real, physically networked,
   multi-node system, you can't switch off the possibility of message loss
   or delay between nodes — it's a fact about the network, not a design
   choice. Martin Kleppmann put it precisely: *"It is misleading to say
   that an algorithm 'provides partition tolerance'... better to say an
   algorithm 'assumes that partitions may occur.'"* — [Kleppmann, "A
   Critique of the CAP Theorem," arXiv:1509.05393 (2015)](https://arxiv.org/abs/1509.05393).

2. **The real choice only happens *during* an actual partition, and only
   for the requests it affects**: wait for a confirmed answer (sacrifice
   Availability, keep Consistency), or answer immediately with whatever
   local data you have (sacrifice Consistency, keep Availability). Eric
   Brewer, the theorem's originator, later wrote that this choice "can
   occur many times within the same system at very fine granularity." —
   [Brewer, "CAP Twelve Years Later: How the 'Rules' Have Changed," IEEE
   Computer 45(2), 2012](https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/brewer-cap.pdf).

3. **"CA" (both Consistency and Availability, no partition tolerance) isn't
   a real category** for a genuinely distributed system. Brewer's own
   resolution: choosing "CA" really just means betting that partitions
   won't happen (e.g. a single datacenter) — and if one happens anyway,
   the system still has to revert to C or A for the affected requests. He
   cites this as a common point of confusion, credited to Daniel Abadi and
   Coda Hale independently making the same objection years earlier.

4. **The formal proof is about atomic (linearizable) consistency, not ACID
   consistency** — a subtly different, stricter meaning. Seth Gilbert and
   Nancy Lynch's 2002 proof states it precisely: *"Discussing atomic
   consistency is somewhat different than talking about an ACID database...
   it subsumes the database notions of both Atomic and Consistent."* —
   [Gilbert & Lynch, "Brewer's Conjecture and the Feasibility of
   Consistent, Available, Partition-Tolerant Web Services," ACM SIGACT News
   33(2), 2002](https://www.cs.cornell.edu/courses/cs6464/2009sp/papers/brewer.pdf).
   Their proof: it's impossible to guarantee both atomic consistency and
   availability once you allow arbitrary message loss between nodes — that
   impossibility is the actual theorem.

5. **Partitions don't have one global "on" state.** Different nodes can
   detect a partition at different times (or not at all); a majority of
   nodes can keep operating completely normally while an isolated minority
   alone enters a degraded mode. This simulation deliberately isolates one
   node at a time rather than flipping a scene-wide "partitioned" switch.

6. **Recovery is its own explicit phase**, not something that happens the
   instant connectivity returns. Brewer's model: detect → enter partition
   mode → recover, where recovery means merging divergent state *and*
   compensating for mistakes made while split. His concrete example: an ATM
   favors availability by allowing withdrawals up to $200 while offline,
   then reconciles balances afterward — possibly charging an overdraft fee
   rather than having blocked the withdrawal in the first place. That's
   exactly what the "reconciling" state and its caption reference.

## What real systems actually do about it

The simulation's two policy buttons ("wait for it" vs. "answer anyway") are
simplified stand-ins for real engineering techniques. Here's what's
actually behind each one, sourced from Amazon's own paper on Dynamo — the
system whose design underlies both Cassandra and DynamoDB:

**Favoring Consistency:**

- **Quorum reads &amp; writes** — require agreement from a majority of
  replicas, not just one, before confirming anything.
- **A single elected leader, kept in sync by a consensus protocol** — route
  all writes through one leader, using an algorithm like **Raft** (etcd) or
  the **Zab** protocol (Apache ZooKeeper) to safely re-elect a new leader
  if the old one disappears, without ever allowing two leaders at once.
- **Distributed locks** — acquire a lock from a majority of nodes before
  changing shared state, so an isolated minority can't also make changes.
- **Just refuse the request** — queue it, time it out, or error — exactly
  what the simulation's "wait" policy shows.

**Favoring Availability**, per Dynamo's own summary of its techniques
(DeCandia et al., 2007, Table 1):

- **Sloppy quorum + hinted handoff** — if the node that should hold some
  data is unreachable, a different reachable node temporarily accepts the
  write (with a "hint" about where it really belongs), then forwards it
  once the original node returns. Dynamo's own words: *"If Dynamo used a
  traditional quorum approach it would be unavailable during server
  failures and network partitions... To remedy this it does not enforce
  strict quorum membership and instead it uses a 'sloppy quorum.'"*
- **Vector clocks** for conflict detection — each version of an object is
  tagged with a list of (node, counter) pairs, so the system can tell "this
  version supersedes that one" apart from "these two changed independently
  and now conflict," the latter requiring reconciliation.
- **CRDTs** (Conflict-free Replicated Data Types) — data structures
  designed so merging two divergent copies happens automatically and
  always lands on the same answer, with nothing left to resolve by hand.
- **Application-level merging** — Dynamo's own shopping-cart example: *"the
  shopping cart application requires that an 'Add to Cart' operation can
  never be forgotten or rejected... When a customer wants to add an item to
  (or remove from) a shopping cart and the latest version is not available,
  the item is added to (or removed from) the older version and the
  divergent versions are reconciled later."* This is why a deleted cart
  item can occasionally reappear.
- **Anti-entropy** using Merkle trees — a background process that compares
  short hash summaries of replicas (instead of every record) to find and
  quietly repair whatever fell out of sync.

**Detecting the partition in the first place:**

- **Failure detection is local, not global** — in Dynamo, *"a purely local
  notion of failure detection is entirely sufficient: node A may consider
  node B failed if node B does not respond to node A's messages."* There's
  no referee announcing "a partition has begun" — which is exactly why this
  simulation never shows one global switch.
- **Gossip protocols** — nodes periodically exchange what they know about
  each other's health/membership with a random peer, so information about
  failures and recoveries spreads through the cluster without a central
  coordinator.

One more simplification worth naming: real systems usually don't make this
choice once for the whole system. Cassandra and DynamoDB let you pick
Consistency or Availability *per request* — critical operations can wait
for a quorum while less critical ones answer immediately, in the same
application, exactly matching Brewer's "fine granularity" point above.

## The bigger picture: PACELC

CAP only describes what happens *during* a partition. Daniel Abadi's
PACELC extension points out that even when nothing is partitioned, systems
still trade off latency against consistency (synchronous replication is
consistent but slow; asynchronous replication is fast but can return stale
reads) — a separate, always-present tradeoff CAP alone doesn't capture. —
[Abadi, "Consistency Tradeoffs in Modern Distributed Database System
Design," IEEE Computer 45(2), 2012](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf).

## Full sources

- Brewer, "Towards Robust Distributed Systems" (PODC 2000 keynote) — [slides, via Wayback Machine](https://web.archive.org/web/2018/http://www.cs.berkeley.edu/~brewer/PODC2000.pdf)
- Gilbert & Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services," ACM SIGACT News, 2002 — [full text](https://www.cs.cornell.edu/courses/cs6464/2009sp/papers/brewer.pdf)
- Brewer, "CAP Twelve Years Later: How the 'Rules' Have Changed," IEEE Computer, 2012 — [full text](https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/brewer-cap.pdf)
- Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design" (PACELC), IEEE Computer, 2012 — [full text](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf)
- Kleppmann, "A Critique of the CAP Theorem," arXiv:1509.05393, 2015 — [full text](https://arxiv.org/abs/1509.05393)
- DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store," ACM SOSP, 2007 — [full text](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
