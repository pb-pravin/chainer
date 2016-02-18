from chainer.trainer import extension


class ExponentialDecay(extension.Extension):

    """Trainer extension to exponentially decay an optimizer attribute.

    This extension exponentially decreases the specified attribute of the
    optimizer. The typical use case is to exponential decay of the learning
    rate.

    Note that this extension is also called before the training loop begins by
    default (i.e. ``invoke_before_training`` flag is True).

    Args:
        attr (str): Name of the attribute to decay.
        decay_rate (float): Rate of the exponential decay. This value is
            multiplied to the attribute at each call.
        init (float): Initial value of the attribute. If it is None, then the
            extension extracts the attribute at the first call and uses it as
            the initial value.
        minimum (float): Minimum value of the attribute. If the attribute
            reaches this value, then the decay stops.
        optimizer (Optimizer): Target optimizer to adjust the attribute. If it
            is None, then the main optimizer of the trainer is used.

    """
    invoke_before_training = True

    def __init__(self, attr, decay_rate, init=None, minimum=None,
                 optimizer=None):
        self._attr = attr
        self._decay_rate = decay_rate
        self._init = init
        self._minimum = minimum
        self._optimizer = optimizer
        self._t = 0

    def __call__(self, trainer):
        optimizer = self._optimizer or trainer.optimizer
        if self._init is None:
            self._init = getattr(optimizer, self._attr)
        value = max(self._init * (self._decay_rate ** self._t),
                    self._minimum)
        setattr(optimizer, self._attr, value)
        self._t += 1

    def serialize(self, serializer):
        self._decay_t = serializer('_t', self._t)
