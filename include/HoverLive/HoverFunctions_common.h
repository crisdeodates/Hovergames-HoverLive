#ifndef HOVERFUNCTIONS_COMMON_H
#define HOVERFUNCTIONS_COMMON_H

#include "HoverIncludes_common.h"

namespace HoverLive {

    namespace uav_modes {
        
    } // namespace uav_modes

    namespace uav_states{

    } // namespace uav_states

    namespace color {

    #define MAKE_COLOR_MANIPULATOR(name, code)                             \
    template < typename CharT, typename Traits = std::char_traits<CharT> > \
    inline std::basic_ostream< CharT, Traits >&                            \
    name(std::basic_ostream< CharT, Traits >& os)                          \
    { return os << code; }

    // These color definitions are based on the color scheme used by Git
    // as declared in the file `git/color.h`. You can add more manipulators as desired.

        MAKE_COLOR_MANIPULATOR( normal       , ""           )

    } // namespace color

} // namespace hoverlive

#endif
