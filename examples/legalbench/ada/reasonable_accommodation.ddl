# ada — "Must an employer provide a reasonable accommodation on request?"  YES.
facts: AccommodationRequest

atom AccommodationRequest: holds when a qualified individual with a disability requests a reasonable accommodation | quote: Upon request
atom ProvideReasonableAccommodation: holds when the employer provides a reasonable accommodation | quote: shall provide a reasonable accommodation to a qualified individual with a disability | uri: examples/legalbench/ada/sources/ada.md#L3

reasonable_accommodation: AccommodationRequest =>O ProvideReasonableAccommodation

# Test:  deontic query <file> ProvideReasonableAccommodation   ->  O(...)   (on request). YES.
