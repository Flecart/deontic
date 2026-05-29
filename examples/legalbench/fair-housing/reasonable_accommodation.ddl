# fair-housing — "Must a provider give a reasonable accommodation on request?"  YES.
facts: AccommodationRequest

atom AccommodationRequest: holds when a person with a disability has requested a reasonable accommodation | quote: Upon request
atom ProvideReasonableAccommodation: holds when the provider grants a reasonable accommodation | quote: shall provide a reasonable accommodation for a person with a disability | uri: examples/legalbench/fair-housing/sources/fha.md#L5

reasonable_accommodation: AccommodationRequest =>O ProvideReasonableAccommodation

# Test:  deontic query <file> ProvideReasonableAccommodation   ->  O(...)   (on request). YES.
