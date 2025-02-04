"use client";
import PropTypes from "prop-types";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";
import { logout } from "@/store/authSlice";

// material-ui
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";

// assets
import EditOutlined from "@ant-design/icons/EditOutlined";
import ProfileOutlined from "@ant-design/icons/ProfileOutlined";
import LogoutOutlined from "@ant-design/icons/LogoutOutlined";
import UserOutlined from "@ant-design/icons/UserOutlined";
import WalletOutlined from "@ant-design/icons/WalletOutlined";

import { ROUTE, ERROR_TEXT } from "@/constants";
import { ToastMessage } from "..";

const PROFILE_MENU = [
  {
    label: "Edit Profile",
    icon: <EditOutlined />,
    indentifier: "EDIT_PROFILE",
  },
  {
    label: "View Profile",
    icon: <UserOutlined />,
    indentifier: "VIEW_PROFILE",
  },
  {
    label: "Social Profile",
    icon: <ProfileOutlined />,
    indentifier: "SOCIAL_PROFILE",
  },
  { label: "Billing", icon: <WalletOutlined />, indentifier: "BILLING" },
  { label: "Logout", icon: <LogoutOutlined />, indentifier: "LOGOUT" },
];

export default function ProfileTab() {
  const [selectedMenu, setSelectedMenu] = useState("");
  const dispatch = useDispatch();
  const router = useRouter();

  const onMenuClick = (event, menuObj) => {
    setSelectedMenu(menuObj.indentifier);
    if (menuObj.indentifier === "LOGOUT") {
      dispatch(logout());
      localStorage.clear();
      router.push(ROUTE.LOGIN);
      ToastMessage("success", ERROR_TEXT.SUCCESSFULLY_LOGOUT);
    }
  };

  return (
    <List
      component="nav"
      sx={{ p: 0, "& .MuiListItemIcon-root": { minWidth: 32 } }}
    >
      {PROFILE_MENU.map((menuObj, i, arr) => {
        return (
          <ListItemButton
            key={i}
            selected={menuObj.indentifier === selectedMenu}
            onClick={(event) => onMenuClick(event, menuObj)}
          >
            <ListItemIcon>{menuObj.icon}</ListItemIcon>
            <ListItemText primary={menuObj.label} />
          </ListItemButton>
        );
      })}
    </List>
  );
}

ProfileTab.propTypes = {
  handleLogout: PropTypes.func,
};
