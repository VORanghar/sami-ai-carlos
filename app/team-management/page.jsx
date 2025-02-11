"use client";
import { Fragment, useState, useEffect } from "react";
import { PageHeader, CustomTable, ConfirmationModal } from "@/components";
import PersonAddAltIcon from "@mui/icons-material/PersonAddAlt";
import withLayout from "@/components/hoc/withLayout";
import { useRouter } from "next/navigation";
import { ROUTE, ROLE_ID_BY_NAME, ACTION_IDENTIFIER } from "@/constants";
import { getApi } from "@/app/api/clientApi";
import { API } from "@/app/api/apiConstant";
import { createData } from "@/utils";
import { useSelector } from "react-redux";
import ToastMessage from "@/components/ToastMessage";
import FileCopyIcon from "@mui/icons-material/FileCopy";
import CreateIcon from "@mui/icons-material/Create";
import DeleteIcon from "@mui/icons-material/Delete";

const TABEL_ACTION = [
  {
    toolTipLabel: "Edit",
    icon: <CreateIcon className="cursor-pointer hover:text-[#005B96]" />,
    identifier: ACTION_IDENTIFIER.EDIT,
  },
  {
    toolTipLabel: "Delete",
    icon: <DeleteIcon className="cursor-pointer hover:text-[#005B96]" />,
    identifier: ACTION_IDENTIFIER.DELETE,
  },
  {
    toolTipLabel: "Clone",
    icon: <FileCopyIcon className="cursor-pointer hover:text-[#005B96]" />,
    identifier: ACTION_IDENTIFIER.CLONE,
  },
];

const TeamManagement = () => {
  const router = useRouter();
  const role_id = useSelector((state) => state?.auth?.role_id);

  const [openConfirmation, setOpenConfirmation] = useState(false);
  const [selectedData, setSelectedData] = useState(null);
  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalCount, setTotalCount] = useState(0);
  const [refresh, setRefresh] = useState(false);
  const [deleteApi, setDeleteApi] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadApi = async () => {
      const { deleteApi } = await import("@/app/api/clientApi");
      setDeleteApi(() => deleteApi);
      setLoading(false);
    };

    loadApi();
  }, []);

  const handleCloseModal = () => {
    setOpenConfirmation(false);
    setSelectedData(null);
  };

  const onActionClick = (event, identifier, row) => {
    switch (identifier) {
      case ACTION_IDENTIFIER.EDIT:
        router.push(`${ROUTE.TEAM_MANAGEMENT}${ROUTE.ADD_EDIT}?id=${row?.id}`);

        break;

      case ACTION_IDENTIFIER.CLONE:
      case ACTION_IDENTIFIER.DELETE:
        setOpenConfirmation(true);
        setSelectedData({ ...row, action: identifier });
        break;

      default:
        ToastMessage("error", "Invalid action identifier");
        break;
    }
  };

  const handleConfirmClick = async (event, identifier) => {
    switch (identifier) {
      case ACTION_IDENTIFIER.DELETE:
        try {
          setLoading(true);
          if (!deleteApi) {
            ToastMessage("error", ERROR_TEXT.API_LOAD_ERROR);
            return;
          }
          const response = await deleteApi(
            `${API.DELETE_USER}/${selectedData?.id}`
          );
          if (response?.error) {
            ToastMessage("error", response?.message);
          } else {
            setRefresh(!refresh);
            ToastMessage("success", response?.data?.message);
          }
        } catch (error) {
          ToastMessage("error", ERROR_TEXT.SOMETHING_WENT_WRONG);
        } finally {
          handleCloseModal();
          setLoading(false);
        }
        break;

      case ACTION_IDENTIFIER.CLONE:
        ToastMessage("error", "Functionality Pending");
        break;

      default:
        ToastMessage("error", "Invalid action identifier");
        break;
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getApi(`${API.GET_USERS}/2`);

        console.log(
          "response?.data?.data?.data==>",
          response?.data?.data?.data
        );

        // if (!response.error) {
        //   const formattedData = response?.data?.data?.data?.map((user) =>
        //     createData(
        //       user.id,
        //       user.name,
        //       user.email,
        //       user.created_at,
        //       user.status
        //     )
        //   );
        //   setTotalCount(response?.data?.data?.total);
        //   setTableData(formattedData);
        // } else {
        //   console.error(response.message);
        // }
      } catch (error) {
        console.error("An unexpected error occurred:", error);
      }
    };

    fetchData();
  }, []);

  const COLUMNS = [
    {
      id: "sno",
      label: "S.No",
      minWidth: 70,
      maxWidth: 70,
      align: "left",
      isVisible: true,
    },
    {
      id: "name",
      label: "Full Name",
      minWidth: 120,
      maxWidth: 120,
      align: "left",
      isVisible: true,
    },
    {
      id: "created_at",
      label: "Registered Date",
      minWidth: 100,
      maxWidth: 100,
      align: "left",
      isVisible: true,
    },
    {
      id: "action",
      label: "Action",
      minWidth: 100,
      maxWidth: 100,
      align: "left",
      isVisible: role_id === ROLE_ID_BY_NAME.ADMIN,
    },
  ];

  return (
    <Fragment>
      <PageHeader
        text="Team Management"
        buttonText={role_id === ROLE_ID_BY_NAME.ADMIN ? "Add Member" : ""}
        onButtonClick={() =>
          router.push(`${ROUTE.TEAM_MANAGEMENT}${ROUTE.ADD_EDIT}`)
        }
        icon={
          <PersonAddAltIcon
            height={20}
            width={20}
            style={{ marginBottom: "4px" }}
          />
        }
      />
      <CustomTable
        ACTION_MENU={TABEL_ACTION}
        onActionClick={onActionClick}
        columns={COLUMNS}
        rows={rows}
        setPage={setPage}
        page={page}
        setRowsPerPage={setRowsPerPage}
        rowsPerPage={rowsPerPage}
        totalCount={totalCount}
      />
      <ConfirmationModal
        open={openConfirmation}
        handleClose={handleCloseModal}
        handleConfirmClick={handleConfirmClick}
        buttontext={selectedData?.action}
        user={{
          user: selectedData?.username,
          userType: "Team Member",
        }}
      />
    </Fragment>
  );
};
export default withLayout(TeamManagement);
