---
title : "Custom hashing architecture"
sidebar:
# Set a custom order for the link (lower numbers are displayed higher up)
  order: 5
---

New method might have a different architecture, our framework also allow custom architecture to be added. This tutorial will provide an example on how to add a new custom architecture.

Firstly, create a new python file at `models/architectures/arch_new.py`. Create a new architecture class extend the base class `BaseArch`. By extending this base class, the following attributes are accessible in the new architecture:
```python
self.backbone_name = config['arch_kwargs']['backbone']
self.nbit = config['arch_kwargs']['nbit']
self.nclass = config['arch_kwargs']['nclass']
self.pretrained = config['arch_kwargs'].get('pretrained', True)
self.freeze_weight = config['arch_kwargs'].get('freeze_weight', False)
self.bias = config['arch_kwargs'].get('bias', False)
self.config = config
self.hash_kwargs = config['loss_param']
```
The new class should created with annotation `@register_network('new_arch_name')` and extending the base class `BaseArch` like the example below:
```python
@register_network('dpn')
class ArchDPN(BaseArch):
    """Arch DPN, CSQ"""
    def __init__(self, config, **kwargs):
        super(ArchDPN, self).__init__(config, **kwargs)

        self.bias = config['arch_kwargs'].get('bias', False)

        self.backbone = get_backbone(backbone=self.backbone_name,
                                     nbit=self.nbit,
                                     nclass=self.nclass,
                                     pretrained=self.pretrained,
                                     freeze_weight=self.freeze_weight,
                                     **kwargs)
        self.ce_fc = nn.Linear(self.backbone.in_features, self.nclass)
        self.hash_fc = nn.Linear(self.backbone.in_features, self.nbit, bias=self.bias)

    def get_features_params(self): # this is a required method
        return self.backbone.get_features_params()

    def get_hash_params(self): # this is a required method
        return list(self.ce_fc.parameters()) + list(self.hash_fc.parameters())

    def forward(self, x): # this is a required method
        x = self.backbone(x)
        u = self.ce_fc(x)
        v = self.hash_fc(x)
        return u, v
```
`get_features_params()` should return the list of trainable parameter from backbone network, while `get_hash_params` should return the list of trainable parameters in the hashing layers. `forward` method should be defined with your computation graph following your architecture.

Then, you should add the created architecture in the whitelist at `supported_model` dict in `constants.py:47`, for example:
```python
supported_model = {
    'orthocos': ['orthohash', 'new_architecture'],
}
```