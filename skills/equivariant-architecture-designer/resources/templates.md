# Equivariant Architecture Code Templates

Ready-to-use code templates for common equivariant architectures.

## Template 1: E(3) Equivariant GNN (e3nn)

For molecular property prediction with E(3) symmetry.

```python
import torch
import torch.nn as nn
from e3nn import o3
from e3nn.nn import FullyConnectedNet, Gate
from e3nn.o3 import FullyConnectedTensorProduct

class E3EquivariantGNN(nn.Module):
    """
    E(3) equivariant graph neural network for molecular modeling.

    Symmetry: E(3) = O(3) x R^3 (rotations, translations, reflections)
    """

    def __init__(
        self,
        irreps_in="1x0e",           # Input: scalar features
        irreps_hidden="32x0e + 8x1o + 4x2e",  # Hidden representations
        irreps_out="1x0e",           # Output: scalar (invariant)
        num_layers=3,
        max_radius=5.0,
        num_basis=8,
    ):
        super().__init__()

        self.irreps_in = o3.Irreps(irreps_in)
        self.irreps_hidden = o3.Irreps(irreps_hidden)
        self.irreps_out = o3.Irreps(irreps_out)

        # Embedding layer
        self.embedding = nn.Linear(
            self.irreps_in.dim,
            self.irreps_hidden.dim
        )

        # Message passing layers
        self.convolutions = nn.ModuleList()
        for _ in range(num_layers):
            self.convolutions.append(
                E3ConvLayer(
                    self.irreps_hidden,
                    self.irreps_hidden,
                    max_radius=max_radius,
                    num_basis=num_basis,
                )
            )

        # Output layer (invariant)
        self.output = nn.Linear(
            self.irreps_hidden.dim,
            self.irreps_out.dim
        )

    def forward(self, node_features, pos, edge_index, batch):
        """
        Args:
            node_features: [N, F] node features
            pos: [N, 3] atom positions
            edge_index: [2, E] edge connectivity
            batch: [N] batch assignment

        Returns:
            [B, output_dim] graph-level predictions
        """
        # Embed input features
        h = self.embedding(node_features)

        # Message passing
        for conv in self.convolutions:
            h = conv(h, pos, edge_index)

        # Global pooling (mean for invariance)
        h = scatter_mean(h, batch, dim=0)

        # Output projection
        return self.output(h)


class E3ConvLayer(nn.Module):
    """Single E(3) equivariant convolution layer."""

    def __init__(self, irreps_in, irreps_out, max_radius, num_basis):
        super().__init__()

        self.irreps_in = o3.Irreps(irreps_in)
        self.irreps_out = o3.Irreps(irreps_out)

        # Spherical harmonics for edge features
        self.irreps_sh = o3.Irreps.spherical_harmonics(lmax=2)

        # Tensor product for message computation
        self.tp = FullyConnectedTensorProduct(
            self.irreps_in,
            self.irreps_sh,
            self.irreps_out,
            shared_weights=False,
        )

        # Radial network
        self.radial_net = FullyConnectedNet(
            [num_basis, 64, self.tp.weight_numel],
            act=torch.nn.functional.silu
        )

        # Radial basis functions
        self.num_basis = num_basis
        self.max_radius = max_radius

    def forward(self, node_features, pos, edge_index):
        src, dst = edge_index

        # Compute edge vectors
        edge_vec = pos[dst] - pos[src]
        edge_length = edge_vec.norm(dim=-1, keepdim=True)

        # Spherical harmonics
        edge_sh = o3.spherical_harmonics(
            self.irreps_sh, edge_vec, normalize=True
        )

        # Radial basis
        edge_basis = self._radial_basis(edge_length)
        edge_weight = self.radial_net(edge_basis)

        # Message passing via tensor product
        messages = self.tp(node_features[src], edge_sh, edge_weight)

        # Aggregate messages
        return scatter_add(messages, dst, dim=0, dim_size=pos.size(0))

    def _radial_basis(self, r):
        """Gaussian radial basis functions."""
        centers = torch.linspace(0, self.max_radius, self.num_basis)
        return torch.exp(-((r - centers) ** 2))
```

## Template 2: Discrete Group CNN (escnn)

For image classification with discrete rotation symmetry.

```python
from escnn import gspaces, nn as enn
import torch.nn as nn

class C4EquivariantCNN(nn.Module):
    """
    CNN equivariant to C4 (90-degree rotations).

    Symmetry: C4 = {0°, 90°, 180°, 270°}
    """

    def __init__(self, num_classes=10):
        super().__init__()

        # Define the group space: C4 acting on R2
        self.gspace = gspaces.rot2dOnR2(N=4)

        # Input: regular scalar field (grayscale image)
        in_type = enn.FieldType(
            self.gspace,
            [self.gspace.trivial_repr]  # 1 channel, trivial representation
        )

        # Feature types
        hidden1 = enn.FieldType(
            self.gspace,
            16 * [self.gspace.regular_repr]  # 16 regular feature fields
        )
        hidden2 = enn.FieldType(
            self.gspace,
            32 * [self.gspace.regular_repr]
        )
        hidden3 = enn.FieldType(
            self.gspace,
            64 * [self.gspace.regular_repr]
        )

        # Build equivariant network
        self.input_type = in_type

        self.block1 = enn.SequentialModule(
            enn.R2Conv(in_type, hidden1, kernel_size=5, padding=2),
            enn.InnerBatchNorm(hidden1),
            enn.ReLU(hidden1, inplace=True),
            enn.PointwiseMaxPool(hidden1, 2),
        )

        self.block2 = enn.SequentialModule(
            enn.R2Conv(hidden1, hidden2, kernel_size=5, padding=2),
            enn.InnerBatchNorm(hidden2),
            enn.ReLU(hidden2, inplace=True),
            enn.PointwiseMaxPool(hidden2, 2),
        )

        self.block3 = enn.SequentialModule(
            enn.R2Conv(hidden2, hidden3, kernel_size=5, padding=2),
            enn.InnerBatchNorm(hidden3),
            enn.ReLU(hidden3, inplace=True),
        )

        # Invariant pooling
        self.pool = enn.GroupPooling(hidden3)

        # Invariant output
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        # Wrap input as geometric tensor
        x = enn.GeometricTensor(x, self.input_type)

        # Equivariant convolutions
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)

        # Pool over group to get invariant features
        x = self.pool(x)

        # Standard classifier
        x = x.tensor  # Extract underlying tensor
        return self.classifier(x)
```

## Template 3: Permutation Invariant Set Network

For set-valued inputs with permutation symmetry.

```python
import torch
import torch.nn as nn

class DeepSets(nn.Module):
    """
    Permutation invariant network for sets (DeepSets).

    Symmetry: S_n (symmetric group, all permutations)
    """

    def __init__(
        self,
        input_dim,
        hidden_dim=64,
        output_dim=1,
        num_layers=3,
    ):
        super().__init__()

        # Per-element encoder (equivariant to permutation)
        encoder_layers = [nn.Linear(input_dim, hidden_dim), nn.ReLU()]
        for _ in range(num_layers - 1):
            encoder_layers.extend([
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU()
            ])
        self.encoder = nn.Sequential(*encoder_layers)

        # Decoder after pooling (invariant)
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        """
        Args:
            x: [B, N, D] set of N elements with D features

        Returns:
            [B, output_dim] set-level prediction
        """
        # Encode each element
        h = self.encoder(x)  # [B, N, hidden_dim]

        # Permutation-invariant aggregation (sum or mean)
        h = h.sum(dim=1)  # [B, hidden_dim]

        # Decode to output
        return self.decoder(h)


class SetTransformer(nn.Module):
    """
    Attention-based permutation invariant network.
    More expressive than DeepSets.
    """

    def __init__(self, input_dim, hidden_dim=64, output_dim=1, num_heads=4):
        super().__init__()

        self.embed = nn.Linear(input_dim, hidden_dim)

        # Self-attention blocks (permutation equivariant)
        self.attention1 = nn.MultiheadAttention(
            hidden_dim, num_heads, batch_first=True
        )
        self.attention2 = nn.MultiheadAttention(
            hidden_dim, num_heads, batch_first=True
        )

        # Layer norms
        self.ln1 = nn.LayerNorm(hidden_dim)
        self.ln2 = nn.LayerNorm(hidden_dim)

        # Pooling via attention to learned query
        self.pool_query = nn.Parameter(torch.randn(1, 1, hidden_dim))
        self.pool_attention = nn.MultiheadAttention(
            hidden_dim, num_heads, batch_first=True
        )

        # Output head
        self.output = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        B = x.size(0)

        # Embed
        h = self.embed(x)

        # Self-attention (equivariant)
        h = h + self.attention1(h, h, h)[0]
        h = self.ln1(h)
        h = h + self.attention2(h, h, h)[0]
        h = self.ln2(h)

        # Pool via attention (invariant)
        query = self.pool_query.expand(B, -1, -1)
        pooled = self.pool_attention(query, h, h)[0].squeeze(1)

        return self.output(pooled)
```

## Template 4: Graph Neural Network (Permutation Equivariant)

```python
import torch
import torch.nn as nn
from torch_geometric.nn import MessagePassing, global_mean_pool

class EquivariantGNN(nn.Module):
    """
    Standard GNN equivariant to node permutations.

    Symmetry: S_n acting on nodes
    """

    def __init__(
        self,
        node_dim,
        edge_dim=0,
        hidden_dim=64,
        output_dim=1,
        num_layers=3,
        task='graph',  # 'graph' or 'node'
    ):
        super().__init__()

        self.task = task

        # Node embedding
        self.node_embed = nn.Linear(node_dim, hidden_dim)

        # Edge embedding (optional)
        self.edge_embed = nn.Linear(edge_dim, hidden_dim) if edge_dim > 0 else None

        # Message passing layers
        self.mp_layers = nn.ModuleList([
            MPLayer(hidden_dim, hidden_dim)
            for _ in range(num_layers)
        ])

        # Output
        self.output = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x, edge_index, edge_attr=None, batch=None):
        # Embed nodes
        h = self.node_embed(x)

        # Embed edges if present
        e = self.edge_embed(edge_attr) if self.edge_embed and edge_attr is not None else None

        # Message passing
        for mp in self.mp_layers:
            h = mp(h, edge_index, e)

        # Task-specific output
        if self.task == 'graph':
            # Global pooling for graph-level prediction
            h = global_mean_pool(h, batch)
        # For node task, h stays as [N, hidden_dim]

        return self.output(h)


class MPLayer(MessagePassing):
    """Single message passing layer."""

    def __init__(self, in_dim, out_dim):
        super().__init__(aggr='add')

        self.mlp = nn.Sequential(
            nn.Linear(2 * in_dim, out_dim),
            nn.ReLU(),
            nn.Linear(out_dim, out_dim),
        )
        self.ln = nn.LayerNorm(out_dim)

    def forward(self, x, edge_index, edge_attr=None):
        out = self.propagate(edge_index, x=x)
        return self.ln(x + out)

    def message(self, x_i, x_j):
        return self.mlp(torch.cat([x_i, x_j], dim=-1))
```

## Usage Notes

### Memory Efficiency
- Higher l irreps (l=3+) are expensive in e3nn
- Start with low l_max and increase if needed
- Use gradient checkpointing for deep networks

### Training Tips
- E(3) networks often need lower learning rates
- Data augmentation is still useful even with built-in equivariance
- Monitor equivariance error during training to catch bugs

### Testing
After implementing, always verify equivariance numerically using the validation suite tests.
