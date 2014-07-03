from ApplianceTrace import ApplianceTrace
from ApplianceInstance import ApplianceInstance
from ApplianceType import ApplianceType
from ApplianceSet import ApplianceSet
from pandas import concat

def concatenate_traces(traces, metadata=None, how="strict"):
    '''
    Given a list of appliance traces, returns a single concatenated
    trace. With how="strict" option, must be sampled at the same rate and
    consecutive, without overlapping datapoints.
    '''
    if not metadata:
        metadata = traces[0].metadata

    if how == "strict":
        # require ordered list of consecutive, similarly sampled traces with no
        # missing data.
        return ApplianceTrace(concat([t.series for t in traces],metadata))
    else:
        raise NotImplementedError

def aggregate_traces(traces, metadata, how="strict"):
    '''
    Given a list of temporally aligned traces, aggregate them into a single
    signal.
    '''
    if how == "strict":
        # require that traces are exactly aligned
        summed_series = traces[0].series
        for trace in traces[1:]:
            summed_series += trace.series
        return ApplianceTrace(summed_series,metadata)
    else:
        return NotImplementedError

def aggregate_instances(instances,how="strict"):
    '''
    Given a list of temporally aligned instances, aggregate them into a single
    signal.
    '''
    if how == "strict":
        traces = [instance.traces for instance in instances]
        traces = [list(t) for t in zip(*traces)] # transpose
        traces = [ aggregate_traces(t,{}) for t in traces]
        # TODO how to aggregate metadata?
        return ApplianceInstance(traces)
    else:
        return NotImplementedError



