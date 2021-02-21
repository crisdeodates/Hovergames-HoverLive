#ifndef HOVERLIVE_H
#define HOVERLIVE_H

#include "HoverFunctions_common.h"

namespace HoverLive {

       class HoverDrone {

           public:
           HoverDrone();
           ~HoverDrone();

           struct control_params {

               // Attitude Parameters
               float roll_deg{}; /**< @brief Roll angle (in degrees, positive is right side down) */
               float pitch_deg{}; /**< @brief Pitch angle (in degrees, positive is nose up) */
               float yaw_deg{}; /**< @brief Yaw angle (in degrees, positive is move nose to the right) */
               float thrust_value{}; /**< @brief Thrust (range: 0 to 1) */

               // AttitudeRate Parameters
               float roll_deg_s{}; /**< @brief Roll angular rate (in degrees/second, positive for
                               clock-wise looking from front) */
               float pitch_deg_s{}; /**< @brief Pitch angular rate (in degrees/second, positive for
                                head/front moving up) */
               float yaw_deg_s{}; /**< @brief Yaw angular rate (in degrees/second, positive for clock-wise
                              looking from above) */

               // Position Parameters
               float north_m{}; /**< @brief Position North (in metres) */
               float east_m{}; /**< @brief Position East (in metres) */
               float down_m{}; /**< @brief Position Down (in metres) */

               // Velocity Parameters
               float forward_m_s{}; /**< @brief Velocity forward (in metres/second) */
               float right_m_s{}; /**< @brief Velocity right (in metres/second) */
               float down_m_s{}; /**< @brief Velocity down (in metres/second) */
               float north_m_s{}; /**< @brief Velocity North (in metres/second) */
               float east_m_s{}; /**< @brief Velocity East (in metres/second) */
               float yawspeed_deg_s{}; /**< @brief Yaw angular rate (in degrees/second, positive for
                                   clock-wise looking from above) */

           };

           };

} // namespace HoverLive

#endif
