 
#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "TelemetryReader.generated.h"

UCLASS()
class BLOCKS_API UTelemetryReader : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:

    UFUNCTION(BlueprintCallable, Category="Telemetry")
    static void ReadDroneTelemetry(
        FString& Status,
        FString& Target,
        FString& Health,
        FString& Intensity,
        int32& Queue
    );
};
