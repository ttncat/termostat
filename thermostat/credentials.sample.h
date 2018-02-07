#define LORA_MODE_ABP   0
#define LORA_MODE_OTAA  1

#define LORA_MODE LORA_MODE_ABP

#if LORA_MODE == LORA_MODE_ABP
    const char *devAddr = "";
    const char *nwkSKey = "";
    const char *appSKey = "";
#endif

#if LORA_MODE == LORA_MODE_OTAA
    const char *appEui = "";
    const char *appKey = "";
#endif
