import numpy as np
from utils import _filter_anomalous_events


def filter_anomalous_events(
        sample,
        source='xform',
        subsample=False,
        random_seed=1,
        p_value_threshold=0.03,
        ref_size=10000,
        channel_labels_or_numbers=None,
        plot=False
):
    """
    Anomalous events are determined via Kolmogorov-Smirnov (KS) statistical
    test performed on each channel. The reference distribution is chosen based on
    the difference from the median.

    :param sample: A FlowKit Sample instance to search for anomalous events
    :param source: data source in the Sample instance to use for detection (generally, transformed events give the
        best results). Valid values are 'raw', 'comp', and 'xform' (see FlowKit documentation for more details).
    :param subsample: Whether to run detection on all events or just the sub-sampled
            events. Default is False (all events)
    :param random_seed: Random seed used for initializing the anomaly detection routine. Default is 1
    :param p_value_threshold: Controls the sensitivity for anomalous event detection. The value is the p-value
        threshold for the KS test. A higher value will filter more events. Default is 0.03
    :param ref_size: The number of reference groups to sample from the 'stable' regions. Default is 3
    :param channel_labels_or_numbers: List of fluorescent channel labels or numbers (not indices)
        to evaluate for anomalous events. If None, then all fluorescent channels will be evaluated.
        Default is None
    :param plot: Whether to plot the intermediate data for the provided channel labels
    :return: list of event indices for anomalous events
    """
    rng = np.random.RandomState(seed=random_seed)

    if source == 'xform':
        events = sample.get_transformed_events(subsample=subsample)
    elif source == 'comp':
        events = sample.get_comp_events(subsample=subsample)
    elif source == 'raw':
        events = sample.get_raw_events(subsample=subsample)
    else:
        raise ValueError("source must be one of 'raw', 'comp', or 'xform'")

    eval_indices = []
    eval_labels = []
    if channel_labels_or_numbers is not None:
        for label_or_num in channel_labels_or_numbers:
            c_idx = sample.get_channel_index(label_or_num)
            eval_indices.append(c_idx)
    else:
        eval_indices = sample.fluoro_indices

    for idx in eval_indices:
        eval_labels.append(sample.pnn_labels[idx])

    anomalous_idx = _filter_anomalous_events(
        events[:, eval_indices],
        eval_labels,
        rng=rng,
        ref_set_count=3,
        p_value_threshold=p_value_threshold,
        ref_size=ref_size,
        plot=plot
    )

    return anomalous_idx
