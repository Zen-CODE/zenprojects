import React from "react";
import { NavBar } from "@components";

import { NavBarProfile } from "./children";
import { LanguageDropdown } from "@util-components";

const AuthNavBar = props => {
  const { t } = props;
  const navigation = [
    {
      id: "welcome",
      icon: "img/icon/apps.svg",
      label: t("navBar.welcome"),
      to: "/welcome"
    },
    {
      id: "profile",
      icon: "img/people.svg",
      label: t("navBar.profile"),
      to: "/profile"
    },
    {
      id: "tunez",
      icon: "img/icon/things.svg",
      label: "Tunez",
      to: "/tunez"
    }

  ];
  return (
    <NavBar
      navigation={navigation}
      sticky={true}
      toolbar={[
        {
          component: () => <LanguageDropdown {...props} />,
          id: "language"
        },
        {
          component: ({open, customClass}) => <NavBarProfile {...props} open={open} customClass={customClass} />,
          id: "profile"
        }
      ]}
    />
  );
};

export default AuthNavBar;
