# ada — "Must an employer engage in the interactive process on request?"  YES.
facts: AccommodationRequest

atom AccommodationRequest: holds when an employee requests a disability accommodation | quote: Upon an accommodation request
atom EngageInteractiveProcess: holds when the employer engages in an interactive process to identify accommodations | quote: shall engage in an interactive process to identify accommodations | uri: examples/legalbench/ada/sources/ada.md#L5

interactive_process: AccommodationRequest =>O EngageInteractiveProcess

# Test:  deontic query <file> EngageInteractiveProcess   ->  O(...)   (on request). YES.
