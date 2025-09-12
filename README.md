# Lisios Integration for Home Assistant

Lisios Integration connects to the Lisios API to provide real-time monitoring of your [Lisios WasserAlarm](https://www.lisios.com/) devices. The WasserAlarm is a smart sensor that attaches to your main water line, helping you detect leaks and monitor water flow.

Once authenticated with your Lisios account, the integration retrieves and displays data from your connected devices:
 - Accelerometer, ambient, and pipe temperature
 - Flow detection status
 - Leakage detection alerts
 - Frost warnings

## 🚀 Installation

### HACS (recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant.
2. **Add** and open the Lisios integration repository in HACS:\
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=nilisos&category=integration&repository=hass-lisios-bridge)
3. Click **Download**.
4. Go to **Settings** and **Restart** Home Assistant.
5. Continue with [**⚙️ Configuration**](#️-configuration).

Alternatively, you can manually add the repository to HACS and install the integration:

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant.
2. Go to **HACS → ⋮ (Overflow menu) → Custom repositories**.
3. Add <https://github.com/nilisos/hass-lisios-bridge> and select type **Integration**.
4. Click **Add** then close the custom repositories dialog.
5. Search for **Lisios** in HACS and click **Download**.
6. Go to **Settings** and **Restart** Home Assistant.
5. Continue with [**⚙️ Configuration**](#️-configuration).

### Manual installation

1. **Download** or clone this repository.
2. **Copy** the `custom_components/lisios` directory into your Home Assistant `custom_components` directory.
3. **Restart** Home Assistant.
5. Continue with [**⚙️ Configuration**](#️-configuration).

## ⚙️ Configuration

1. Start the Lisios integration setup:\
   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=lisios)
2. **Log in** with your Lisios username and password.

Alternatively, you can manually open the integration setup:

1. Go to **Settings → Devices & services → Add integration**.
2. Search for and select **Lisios**.
3. **Log in** with your Lisios username and password.
