/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * > : Request send to card
  * < : Response from card
  * \ :
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */


/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

SMARTCARD_HandleTypeDef hsc1;
UART_HandleTypeDef huart2;
SMARTCARD_HandleTypeDef hsc3;

/* USER CODE BEGIN PV */
uint8_t sWelcome[] = "Authentication completed\r\n";
uint8_t sPassword[] = "secret";
uint8_t bootMsg[] = "Booting STM32 Cortex-Mx\r\n";

uint8_t promptMsg[] = "Enter password: \r\n";
uint8_t endMsg[1000] = "\r\n[!] Memory dumping completed successfully...";

uint8_t CLRSCR[] = "\033[0H\033[0J";
int authenticationFlag = 1;


/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_USART1_SMARTCARD_Init(void);
static void MX_USART3_SMARTCARD_Init(void);
/* USER CODE BEGIN PFP */


/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */


void secretFunction() {
	HAL_UART_Transmit(&huart2, sWelcome, strlen(sWelcome), 100);

	while(1){
		HAL_GPIO_TogglePin(LED_GPIO_Port,LED_Pin);
		HAL_Delay(100);

	}

}


void uartPoll() {
	uint8_t byte;
	int offset = 0;
	char buffer[20] = { 0 };

	while (1) {
		if (HAL_UART_Receive(&huart2, &byte, 1, 0) == HAL_OK) {
			if (byte == '\r' || byte == '\n') {
				buffer[offset] = 0; // null terminated string
				if (strcmp(sPassword, buffer) == 0) {
					authenticationFlag = 0;
				}
				offset = 0;
				return;
			} else {
				buffer[offset] = byte;
				offset++;
			}
		}
	}
}


/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_USART2_UART_Init();
  MX_USART1_SMARTCARD_Init();
  MX_USART3_SMARTCARD_Init();
  /* USER CODE BEGIN 2 */

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	  uartPoll();

	  if(!authenticationFlag)
	  {
		  secretFunction();
	  }

	  HAL_Delay(100);

  }
  /* USER CODE END 3 */
}
