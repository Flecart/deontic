# Example 5 (Governatori 2018): Australian Road Rules, sect. 40.
# Prohibition + a permissive defeater giving strong permission.
# Try:  ddl query examples/uturn.ddl "F Uturn" --facts "AtTrafficLights."
#       ddl query examples/uturn.ddl "Ps Uturn" \
#         --facts "AtTrafficLights. UturnPermittedSign."

arr40a: AtTrafficLights    =>O -Uturn   # must not U-turn at traffic lights
arr40e: UturnPermittedSign ~>O Uturn    # a permitted-sign derogates the prohibition

arr40a < arr40e
