# Ablation Tables

For each major construct: what would break if you removed each piece. The single most pedagogically valuable step in decoding — these are the answers that build *durable* understanding.

## Contents
- Self-attention
- LayerNorm
- Softmax
- Cross-entropy
- Convolution
- ResNet block
- Dropout
- Diffusion
- Adam optimizer
- Contrastive loss
- VAE

---

## Self-attention

| Remove | What happens | What insight it reveals |
|---|---|---|
| Softmax | Output becomes a linear combination — every token mixed with every other, no selectivity | Softmax is what makes attention *attention* and not averaging |
| √d scaling | At high d, dot products grow large in magnitude, softmax saturates, gradients vanish | √d controls the variance of scores so softmax stays in its useful (non-saturated) regime |
| Separate Q vs K | Tokens can only attend based on self-similarity | Splitting Q and K is what allows asymmetric matching ("X asks for Y, Y advertises for X") |
| V (use K instead) | Model can only retrieve what tokens advertise about themselves; no separate "content" channel | V is the actual payload — separate from the matching key, allowing rich content unrelated to the matching criterion |
| Multi-head (use single big head) | Single semantic relation per layer; loses ability to attend along multiple axes simultaneously | Heads parallelize attention over multiple subspaces, allowing simultaneous specialization |
| Linear projections (Q = K = V = X) | Whole layer reduces to a low-rank, fixed-similarity averaging | The projections are what *learn* what to ask, advertise, and deliver |

---

## LayerNorm

| Remove | What happens | What insight it reveals |
|---|---|---|
| Centering (mean subtraction) | Activations drift; downstream layers see shifting input distributions | Centering is the cheap fix for input-mean drift across training |
| Rescaling (std division) | Activations explode or vanish at different rates per layer | Rescaling tames the magnitude so deep stacks remain trainable |
| Learnable γ | Outputs are forced to unit variance — sometimes the next layer wants more variance | γ recovers the expressive freedom that strict normalization removed |
| Learnable β | Outputs are forced to zero mean — sometimes the next layer wants a non-zero mean | β recovers the expressive freedom that centering removed |
| Whole LayerNorm | Deep networks become much harder to train; small changes in early layers compound badly | LayerNorm's job is to *cap* the badness of activation drift, decoupling layers' optimization |

---

## Softmax

| Remove | What happens | What insight it reveals |
|---|---|---|
| Exp (use raw scores + normalize) | Negative scores produce negative "probabilities"; positivity broken | Exp ensures positivity in a smooth, monotone way |
| Normalize | Outputs no longer sum to 1; downstream cross-entropy breaks | Normalize is what makes softmax a *distribution*, not just a positivity wrapper |
| Use linear sigmoid instead | Loses sharpness scaling — sigmoid doesn't amplify contrast the way exp does | Exp's amplification is what makes softmax sharper at high contrast and smoother at low contrast |

---

## Cross-entropy

| Remove | What happens | What insight it reveals |
|---|---|---|
| Log | Loss becomes squared error or similar; doesn't strongly punish near-zero probability on the truth | The log is what blows up when q assigns near-zero probability to a true outcome |
| Weighting by p (use uniform) | Loss measures total log-prob across all classes equally, ignoring which class is actually true | Weighting by p focuses the loss on the *truth* — this is what makes it correct for one-hot classification |
| Negative sign | Loss prefers low log-prob — opposite of what you want | The negative sign converts "log-prob you want to maximize" into "loss you want to minimize" |

---

## Convolution

| Remove | What happens | What insight it reveals |
|---|---|---|
| Weight sharing (use unique weights per position) | Becomes locally-connected layer; loses translation equivariance, parameter count explodes | Weight sharing *is* the translation equivariance prior; it's the most important inductive bias of conv |
| Locality (full receptive field per position) | Becomes a fully-connected layer; loses spatial structure exploitation, parameter count explodes more | Locality is the prior that "nearby pixels matter most" |
| Stride / pooling | Output is the same spatial size as input; lose multi-scale feature extraction | Downsampling is what builds the hierarchy of receptive field sizes |
| Multiple channels (use 1) | Each layer can only learn one feature map | Multiple output channels = multiple parallel feature detectors at the same scale |

---

## ResNet block

| Remove | What happens | What insight it reveals |
|---|---|---|
| Identity skip | Very deep networks become nearly untrainable; gradients vanish through stacks of nonlinearities | The skip is the gradient highway — without it, depth becomes destructive |
| Learnable f (just identity) | Every layer is a no-op; whole network can't learn anything | f is where the actual learning happens; the skip is *only* an aid, not a replacement |
| Sum (use concat instead) | Channel count grows with depth; computationally expensive; loses the "small correction" interpretation | The sum makes f a *delta* added to x, so f can be small and still useful |

---

## Dropout

| Remove | What happens | What insight it reveals |
|---|---|---|
| The mask | No regularization; network can co-adapt freely on training data, leading to overfitting | The random mask forces redundancy across neurons |
| Rescaling (1/keep_prob) | Train and inference activation scales mismatch; predictions are systematically wrong at inference | The rescale keeps expected activation the same with or without dropout, making the train/test gap clean |

---

## Diffusion (one step)

| Remove | What happens | What insight it reveals |
|---|---|---|
| Noise schedule (use single noise level) | Denoising target is too hard; one step from pure noise to clean image is asking for too much | The schedule decomposes a hard generation task into many easy denoising tasks |
| Time conditioning of denoiser | Denoiser must be the same function at all noise levels — forced to compromise | Conditioning on t lets the denoiser specialize: subtle refinements at low t, coarse structure at high t |
| Multiple sampling steps (use one) | Sample quality crashes; output is blurry, lacks detail | Many small denoising steps allow the model to gradually shape noise into structure |
| Stochastic sampling (use deterministic) | Reduces sample diversity but often improves single-sample quality (this is DDIM vs DDPM) | The sampling stochasticity is a *trade-off knob* between diversity and quality |

---

## Adam optimizer

| Remove | What happens | What insight it reveals |
|---|---|---|
| First moment (m, momentum) | Updates become more noisy; convergence is slower in flat regions | Momentum smooths noisy gradients, accelerating in consistent directions |
| Second moment (v, per-coord scaling) | All parameters get the same effective learning rate — embeddings update at the same rate as LayerNorm γ, badly | Per-coord rescaling is what gives Adam its "no manual tuning per parameter" reputation |
| Bias correction (m̂, v̂) | Early in training, m and v are small (initialized to 0), so updates are systematically too small | Bias correction fixes the cold-start issue — without it, you'd need a long warmup |
| ε in denominator | Division by zero when v = 0 (parameter never moved) | ε is just a numerical safety; tiny conceptually |

---

## Contrastive loss (InfoNCE)

| Remove | What happens | What insight it reveals |
|---|---|---|
| Negatives (just minimize sim(z, z⁺)) | Trivial solution: collapse all z to a constant; sim(z, z⁺) is maximized | Negatives are what *prevent* collapse — they force z to remain distinguishable |
| Softmax / cross-entropy structure (use raw similarity) | No relative scaling; magnitude of similarity dominates and signal-to-noise is poor | Softmax converts absolute similarities into relative weights, which is what cross-entropy needs |
| Temperature τ (use 1) | Loss may be too smooth (large τ) or too sharp (small τ) for the task | τ tunes how aggressively close negatives are pushed away — a critical hyperparameter |

---

## VAE

| Remove | What happens | What insight it reveals |
|---|---|---|
| KL regularizer | Latent space collapses into disjoint clusters around each training x; sampling produces noise | The KL is what forces latent overlap, which is what makes the space *generative* (samplable) |
| Reconstruction term | Encoder is free to ignore x entirely; latent posterior matches the prior trivially (posterior collapse) | The reconstruction term is what forces the latent to actually carry information about x |
| Reparameterization trick | Sampling z is non-differentiable; can't backprop through the encoder | Reparam is the trick that makes the entire VAE differentiable — without it, you'd need REINFORCE or similar |
| Stochastic z (use deterministic z = μ) | Becomes a regular autoencoder; loses smoothness of latent space, can't sample new x | The stochasticity is what forces the latent to be a *distribution* with well-defined smooth structure |
