---
title : "Custom Backbone"
sidebar:
# Set a custom order for the link (lower numbers are displayed higher up)
  order: 4
---

In this framework, we have implemented 3 popular backbone network, which are AlexNet, VGG, and ResNet. We also leave the option to add other backbone network.
This tutorial will give an example to implement a custom backbone network.

First, create a new python file `models/backbone/new_backbone.py`. Inside, create a new Backbone network extending the base class `BaseBackbone`. For example,
```python
class NewAlexNetBackbone(BaseBackbone):
    def __init__(self, nbit, nclass, pretrained=False, freeze_weight=False, **kwargs):
        super(NewAlexNetBackbone, self).__init__()

        model = alexnet(pretrained=pretrained)
        self.features = model.features
        self.avgpool = model.avgpool
        fc = []
        for i in range(6):
            fc.append(model.classifier[i])
        self.fc = nn.Sequential(*fc)
        self.classifier = model.classifier[-1]

        self.in_features = model.classifier[6].in_features
        self.nbit = nbit
        self.nclass = nclass

        if freeze_weight:
            for param in self.features.parameters():
                param.requires_grad_(False)
            for param in self.fc.parameters():
                param.requires_grad_(False)

    def get_features_params(self): # this is required method
        return list(self.features.parameters()) + list(self.fc.parameters()) + list(self.classifier.parameters())

    def get_hash_params(self): # this is required method
        raise NotImplementedError('no hash layer in backbone')

    def train(self, mode=True):
        super(NewAlexNetBackbone, self).train(mode)

        # all dropout set to eval
        for mod in self.modules():
            if isinstance(mod, nn.Dropout):
                mod.eval()

    def forward(self, x): # this is required method
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
```
Secondly, in `models.architectures.helper.get_backbone` add the definition(s) of your new custom backbone, for example:
```python
if backbone == 'alexnet':
    return AlexNetBackbone(nbit=nbit, nclass=nclass, pretrained=pretrained,
                           freeze_weight=freeze_weight, **kwargs)
if backbone == 'new_alexnet':
    return NewAlexNetBackbone(nbit=nbit, nclass=nclass, pretrained=pretrained,
                              freeze_weight=freeze_weight, **kwargs)

```