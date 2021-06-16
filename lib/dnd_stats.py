def trim_bins(bins, data):
    return [x for x in bins if x <= max(data)+1]