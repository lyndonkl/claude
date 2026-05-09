# Decoded Constructs

Full decodes of common ML constructs, ready to deliver. Each follows the workflow: formula → primitives → contributions → composition → punchline.

## Contents
- Self-attention
- Multi-head attention
- LayerNorm
- BatchNorm
- Softmax
- Cross-entropy
- Convolution layer
- ResNet block / residual connection
- Dropout
- Diffusion (one denoising step)
- SGD update
- Adam update
- Embedding lookup
- Contrastive loss (InfoNCE)
- KL divergence
- VAE (one forward pass)

---

## Self-attention

**Formula:** Output = softmax(QKᵀ / √d) · V, where Q = X·W_Q, K = X·W_K, V = X·W_V, and d is the per-head key dimension.

**Primitives:**
1. **Linear projections × 3** (Q, K, V are three different learnable linear layers applied to the same input X).
2. **Dot product** (QKᵀ scores every (query, key) pair).
3. **Scaled softmax** (divide by √d, then row-normalize into mixing weights).
4. **Weighted sum** (multiplying by V averages value vectors with the softmax weights).

**Contributions:**
1. Q, K, V projections give each token three roles: a *question* (Q), an *advertisement* (K), and a *deliverable* (V). The split is what makes attention work — using one vector for all three would force the network to ask, advertise, and deliver the same thing.
2. The dot product turns "alignment between question and advertisement" into a scalar score.
3. The √d divisor keeps the variance of scores bounded as d grows, so softmax stays in its useful regime (not too saturated). Softmax then turns raw scores into mixing weights that sum to 1.
4. The weighted sum collects each token's softmax-weighted view of all value vectors.

**Why it works:** Self-attention is content-addressable retrieval implemented in pure linear algebra. Each token looks up the value vectors in proportion to how well its query matches each key. The whole transformer is just stacks of this lookup mixed with FFNs.

---

## Multi-head attention

**Formula:** Output = Concat(head₁, …, head_h) · W_O, where head_i = Attention(X·W_Q^i, X·W_K^i, X·W_V^i).

**Primitives:**
1. **Self-attention × h** (h independent attention computations, each on a different learned subspace).
2. **Concatenation** (stack the h outputs along the feature axis).
3. **Linear projection** (W_O mixes information across heads).

**Contributions:**
1. Each head is a self-attention computation on a smaller subspace. Different heads can learn to attend along different relations (e.g., head 1 = local syntax, head 2 = long-range semantics).
2. Concatenation glues their outputs into one wide vector.
3. W_O lets the next layer combine head outputs in a learned way.

**Why it works:** Single-head attention is forced to compress all relational types into one set of weights. Multi-head provides parallel "attention channels", each free to specialize, then combines them — much like multi-scale features in conv nets.

---

## LayerNorm

**Formula:** LN(x) = γ · (x − μ) / σ + β, where μ = mean(x), σ = std(x), and γ, β are learnable per-feature scalars.

**Primitives:**
1. **Centering** (subtract the mean).
2. **Rescaling** (divide by std).
3. **Learnable affine** (γ · result + β).

**Contributions:**
1. Centering puts the activation cloud at the origin.
2. Rescaling squeezes it to unit variance.
3. The learnable γ, β allow the network to *redo* any shift and scale that's actually useful for the next layer — so layer norm doesn't strip expressiveness, it just gives the optimizer a stable starting point.

**Why it works:** Optimization is much easier when each layer's input distribution is well-behaved. LayerNorm forces it to be well-behaved at every layer, every step. The learnable affine recovers any expressive shift/scale the network actually needs.

---

## BatchNorm

**Formula:** BN(x) = γ · (x − μ_batch) / σ_batch + β, where μ_batch and σ_batch are computed across the batch (per feature).

**Primitives:** same as LayerNorm, but the statistics are computed per *feature, across the batch* (BN) instead of per *example, across features* (LN).

**Contributions:** Identical mechanism; the difference is *what gets normalized together*. BN normalizes "this feature, across the batch"; LN normalizes "this example, across features".

**Why it works:** Same reason as LN — stable input distributions. BN was the first; LN replaced it in transformers because BN behaves badly with small batches and variable-length sequences.

---

## Softmax

**Formula:** softmax(x)ᵢ = exp(xᵢ) / Σⱼ exp(xⱼ).

**Primitives:**
1. **Element-wise exponential** (positivity).
2. **Normalize** (sum-to-1).

**Contributions:**
1. Exp makes everything positive *and* amplifies score differences.
2. Normalization places the result on the simplex.

**Why it works:** It's a *soft argmax*. At high contrast (one score much bigger), it concentrates near a corner of the simplex (one outcome). At low contrast (scores close), it spreads near the center (uniform). The "softness" comes from the smooth transition between those two regimes — which is what makes it differentiable, hence trainable.

---

## Cross-entropy

**Formula:** H(p, q) = −Σᵢ pᵢ log qᵢ.

**Primitives:**
1. **Log** (turns the predicted probability into a log-probability — i.e., negative surprise).
2. **Weighted sum** (weights the surprise of each outcome by how often it actually happens, under p).

**Contributions:**
1. Log of a probability between 0 and 1 is negative; the closer to 0, the more negative. So −log q(true class) is a "surprise" measure that blows up when q assigns near-zero probability to the truth.
2. Weighting by p means: only outcomes that actually happen contribute. For a one-hot p, the formula collapses to −log q(true class).

**Why it works:** It's the unique loss that's both correctly calibrated for probabilistic predictions and tractable to differentiate. It punishes a model especially hard for being confidently wrong on the true class.

---

## Convolution layer

**Formula:** output[i, j, c_out] = Σ_{k, l, c_in} kernel[k, l, c_in, c_out] · input[i+k, j+l, c_in].

**Primitives:**
1. **Linear projection** (the kernel weights × the local patch is a dot product).
2. **Weight sharing** (the same kernel is reused at every spatial position).

**Contributions:**
1. The dot product at each position measures "how much does the local patch here look like this kernel?"
2. Weight sharing means the same feature detector is applied everywhere — the layer is *translation-equivariant* (shift the input → output shifts by the same amount). It also reduces parameters massively.

**Why it works:** Conv is "what would a fully-connected layer look like if you knew, in advance, that the same feature might appear at any position?" Weight sharing imposes this prior, making the model both more sample-efficient and translation-equivariant.

---

## ResNet block / residual connection

**Formula:** y = x + f(x), where f is some learnable transformation (typically two conv layers + nonlinearities).

**Primitives:**
1. **Learnable transformation** f.
2. **Identity** (x passed through unchanged).
3. **Sum** (add them).

**Contributions:**
1. f learns a *correction* or *delta* — what to add to x.
2. The identity path means gradients flow back even when f is small or saturated.
3. The sum combines them.

**Why it works:** Without the residual, very deep networks suffer because gradients must travel through every nonlinear transformation to reach early layers, and they decay. The identity path provides a "gradient highway" that always backpropagates cleanly. As a bonus, the network can easily learn "do nothing" by setting f ≈ 0, which lets you safely add depth.

---

## Dropout

**Formula:** During training: output = x · mask · (1/keep_prob), where mask is a random binary tensor with each entry = 1 with probability keep_prob.

**Primitives:**
1. **Random binary mask** (Bernoulli noise injection).
2. **Rescaling** (1/keep_prob, to preserve expected value).

**Contributions:**
1. Randomly zeroing some activations forces the network to not rely on any single neuron.
2. Rescaling keeps activations in the same range whether or not dropout is active, so train and inference behave consistently.

**Why it works:** It's an ensemble in disguise — each forward pass uses a randomly-thinned subnetwork. The full network at inference time is approximately the average of all those subnetworks. Forces redundancy; prevents co-adaptation.

---

## Diffusion (one denoising step)

**Formula:** x_{t-1} = denoiser(x_t, t) — typically: predict noise ε from x_t, then x_{t-1} = (x_t − scale · ε) / norm.

**Primitives:**
1. **Noise injection (forward process)** — used during training only: x_t = √α x_0 + √(1−α) ε, with ε ∼ N(0, I).
2. **Neural denoiser** — usually a U-Net: linear projections + nonlinearities + attention.
3. **Sampling step** — algebraic combination of x_t and predicted ε to get x_{t-1}.

**Contributions:**
1. The forward process gives infinite paired (clean, noisy) examples at every noise level — free training data.
2. The denoiser is just regression: given x_t, predict ε. No fancy distribution modeling.
3. Iterating the step from t = T down to t = 0 turns pure noise into a clean sample.

**Why it works:** Direct generation is hard because the target distribution is complicated. Diffusion replaces it with many easy denoising regressions, each only one noise-level step. The slow schedule gives the network enough capacity to gradually shape noise into structure.

---

## SGD update

**Formula:** θ ← θ − η · ∇_θ L.

**Primitives:**
1. **Gradient computation** (backprop).
2. **Scaled subtraction** (move in the negative gradient direction by step size η).

**Contributions:**
1. The gradient is the direction of steepest *ascent* of the loss.
2. Subtracting takes a step in the steepest *descent* direction. η controls how far.

**Why it works:** Local descent on the loss surface. With small enough η and well-behaved loss, you converge to a critical point. In practice, the surface is non-convex and full of saddle points, but SGD's stochasticity helps escape them.

---

## Adam update

**Formula:** m ← β₁m + (1−β₁)g; v ← β₂v + (1−β₂)g²; θ ← θ − η · m̂/(√v̂ + ε).

**Primitives:**
1. **Gradient** g.
2. **EMA of gradient** (m: first moment, smooths the gradient over time).
3. **EMA of squared gradient** (v: second moment, tracks per-coordinate gradient magnitude).
4. **Per-coordinate rescaling** (m / √v: divide by the typical magnitude per dimension).
5. **Scaled subtraction** (with bias-corrected versions m̂, v̂).

**Contributions:**
1. m smooths noisy gradients across steps.
2. v tracks how active each parameter has been.
3. Dividing m by √v gives each parameter its own effective learning rate — large for parameters with small gradients, small for parameters with big ones.
4. The scaled subtraction takes the actual step.

**Why it works:** Different parameters have very different gradient scales (e.g., embeddings vs LayerNorm γ). A single learning rate either overshoots some or undershoots others. Adam adapts per-coordinate based on observed gradient statistics — usually faster convergence and less hyperparameter sensitivity than SGD.

---

## Embedding lookup

**Formula:** emb[i] = E[i, :], where E is a learnable matrix of shape (vocab_size, dim).

**Primitives:**
1. **Index** (select row i).
2. **Learnable table** (the matrix E).

**Contributions:**
1. The index turns a discrete token (an integer) into a row selection.
2. The table is just learnable parameters — no nonlinearity, no projection. Each row is a learned coordinate for one token.

**Why it works:** Most ML architectures want vectors. Embedding gives every discrete object a learnable continuous coordinate. After training, *distance and direction in this space are meaningful* — the loss made them so.

---

## Contrastive loss (InfoNCE)

**Formula:** L = −log[exp(sim(z, z⁺)/τ) / Σⱼ exp(sim(z, zⱼ)/τ)], where z⁺ is a positive (paired) sample and the sum is over the positive plus all negatives.

**Primitives:**
1. **Similarity function** (usually dot product or cosine).
2. **Temperature scaling** (divide by τ; controls sharpness like in softmax).
3. **Softmax** (over similarities).
4. **Cross-entropy** (treating the positive as the "correct class").

**Contributions:**
1. sim(z, z⁺) measures alignment between the anchor and its positive pair.
2. Dividing by τ controls how sharply the softmax distinguishes positive from negatives.
3. Softmax converts raw similarities into mixing weights.
4. Cross-entropy says "the positive pair should get all the probability".

**Why it works:** It's classification with the positive as the correct class and the negatives as wrong classes. Minimizing the loss *pulls* z and z⁺ together (high similarity) and *pushes* z and the negatives apart (low similarity). All in one differentiable loss.

---

## KL divergence

**Formula:** KL(p ‖ q) = Σ p(x) log[p(x) / q(x)].

**Primitives:**
1. **Log-ratio** (log[p/q]).
2. **Weighted sum** under p.

**Contributions:**
1. log[p/q] is positive when p > q, negative when p < q. Big magnitude when they differ a lot.
2. Weighting by p means: the average log-ratio is taken under the distribution that's "true". Asymmetry comes from this.

**Why it works:** It's the expected log-likelihood ratio: "if you sampled from p but assumed q, on average how surprised would you be (relative to assuming p correctly)?" Always non-negative; zero iff p = q. Asymmetric because the expectation is taken under one distribution, not both.

---

## VAE (one forward pass)

**Formula:** z ∼ N(μ_φ(x), σ_φ(x)²); x̂ = decoder_θ(z); loss = recon(x, x̂) + KL(q_φ(z|x) ‖ N(0, I)).

**Primitives:**
1. **Encoder** (neural network producing μ, σ from x).
2. **Reparameterization trick** (z = μ + σ · ε, ε ∼ N(0, I)).
3. **Decoder** (neural network reconstructing x from z).
4. **Reconstruction loss** (MSE or cross-entropy between x and x̂).
5. **KL divergence regularizer** (push posterior toward standard normal prior).

**Contributions:**
1. Encoder maps x to a distribution (not a point) in latent space.
2. Reparameterization makes the random sampling step differentiable.
3. Decoder reconstructs x from any sample in latent space.
4. Reconstruction loss makes the autoencoder actually preserve information.
5. KL regularizer keeps the latent space from collapsing to disjoint Gaussians around each x — instead, it forces overlap, so neighboring points decode to similar x's.

**Why it works:** The reconstruction term wants the latent space to memorize each x; the KL term wants it to be a smooth standard normal. The tradeoff produces a *smooth*, *generative* latent space — sample any point in it, decode, get a plausible new x.
