import { safeStorage } from 'electron'
import Store from 'electron-store'

const store = new Store()

export class SecureStorage {
  /**
   * Encrypts and stores an API key securely in the OS keychain.
   * @param providerId The ID of the provider (e.g., 'openai', 'anthropic')
   * @param apiKey The plaintext API key
   */
  static storeKey(providerId: string, apiKey: string): boolean {
    try {
      if (safeStorage.isEncryptionAvailable()) {
        const encryptedKey = safeStorage.encryptString(apiKey)
        store.set(`api_keys.${providerId}`, encryptedKey.toString('base64'))

        return true
      } else {
        // Fallback for systems without keychain support (not recommended for production)
        store.set(`api_keys.${providerId}`, apiKey)

        return false
      }
    } catch (error) {
      console.error(`Failed to store key for ${providerId}:`, error)

      return false
    }
  }

  /**
   * Retrieves and decrypts an API key from the OS keychain.
   * @param providerId The ID of the provider
   */
  static retrieveKey(providerId: string): string | null {
    try {
      const storedKey = store.get(`api_keys.${providerId}`) as string | undefined

      if (!storedKey) {
        return null
      }

      if (safeStorage.isEncryptionAvailable()) {
        const encryptedBuffer = Buffer.from(storedKey, 'base64')

        return safeStorage.decryptString(encryptedBuffer)
      } else {
        return storedKey
      }
    } catch (error) {
      console.error(`Failed to retrieve key for ${providerId}:`, error)

      return null
    }
  }

  /**
   * Removes an API key from secure storage.
   * @param providerId The ID of the provider
   */
  static removeKey(providerId: string): void {
    store.delete(`api_keys.${providerId}`)
  }
}
