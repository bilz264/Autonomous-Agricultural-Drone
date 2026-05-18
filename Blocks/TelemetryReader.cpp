#include "TelemetryReader.h"

#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonReader.h"

void UTelemetryReader::ReadDroneTelemetry(
    FString& Status,
    FString& Target,
    FString& Health,
    FString& Intensity,
    int32& Queue
)
{
    FString JsonString;

    FString FilePath =
        TEXT("/home/user/AirSim/PythonClient/multirotor/drone_status.json");

    if (FFileHelper::LoadFileToString(JsonString, *FilePath))
    {
        TSharedPtr<FJsonObject> JsonObject;

        TSharedRef<TJsonReader<>> Reader =
            TJsonReaderFactory<>::Create(JsonString);

        if (FJsonSerializer::Deserialize(Reader, JsonObject)
            && JsonObject.IsValid())
        {
            Status =
                JsonObject->GetStringField("status");

            Target =
                JsonObject->GetStringField("target");

            Health =
                JsonObject->GetStringField("health");

            Intensity =
                JsonObject->GetStringField("intensity");

            Queue =
                JsonObject->GetIntegerField("queue");

            return;
        }
    }

    Status = "NO DATA";
    Target = "NONE";
    Health = "NONE";
    Intensity = "0%";
    Queue = 0;
}
