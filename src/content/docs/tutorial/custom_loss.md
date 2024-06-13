---
title : "Custom Loss"
sidebar:
# Set a custom order for the link (lower numbers are displayed higher up)
  order: 6
---

First, create a new python file `functions/loss/new_loss.py`. Create the loss class like the example below:
```python
class NewLoss(nn.Module):
    def __init__(self, **kwargs):
        super(NewLoss, self).__init__()

        self.losses = {}  # required field

    def forward(self, x, h, b, labels, index, **kwargs):
        """
        x: features before hash layer
        h: output from hash FC
        b: binary code
        labels: not using (only use to obtain size)
        """
        
        loss1 = F.mse_loss(target_b, target_x)
        loss2 = ..
        loss = loss1+ loss2
        
        self.losses['mse'] = loss1  # to display and record the loss
        self.losses['loss2'] = loss2
        return loss
```
```{note}
The parameter for forward method will be different depends on type of the loss, the example above is for `unsupervised` method.
```
| Method type  | Loss params                                    |
|--------------|------------------------------------------------|
| supervised   | self, logits, code_logits, labels, onehot=True |
| unsupervised | self, x, h, b, labels, index, **kwargs         |
| pairwise     | self, u, y, ind=None                           |
| adversarial  | self, x, code_logits, rec_x, discs             |
| shallow      | self, x                                        |
| contrastive  | self, prob_i, prob_j, z_i, z_j                 |

The parameter could also differ from the default, but that will be out of the scope of this example.

Secondly, at `scripts.train_helper.get_loss`, in `loss` dict, add the new loss name and link it to the loss class. For example:
```python
loss = {
    'orthocos': OrthoCosLoss,
    'new_loss': NewLoss,
    ...
}
```
Then, at `losses` dict in `constants.py:28`, add the new loss name to the type of loss, for example, `new_loss` is a type of `supervised` loss/method:
```python
losses = {
    'supervised': ['orthocos', ...,  'new_loss'],
    ...
}
```
Lastly, add the created loss and their supported architecture in the whitelist at `supported_model` dict in `constants.py:47`, for example:
```python
supported_model = {
    'new_loss': ['orthohash', 'new_architecture'],
}
```