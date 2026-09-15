def batch_pill(batch):
    css_class = "batch-" + batch.lower().replace(" ", "-")
    return f'<span class="batch-pill {css_class}">{batch}</span>'

def timing_pill(timing):
    css_class = "timing-" + timing.replace(":", "-")
    return f'<span class="batch-pill {css_class}">{timing}</span>'