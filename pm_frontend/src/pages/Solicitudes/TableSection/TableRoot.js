// React core
import { useContext, useEffect } from 'react';
// @mui
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
// Parts of the component
import ButtonActions from 'pages/Solicitudes/TableSection/ButtonActions'
// Context
import FiltersContext from 'context/FiltersContext';
// custom hooks
import { useBackend } from 'hooks/useBackend';

export default function TableRoot () {
  const { getRequests } = useBackend();
  const { filters, listRequests, setListRequests } = useContext(FiltersContext);
  const rows = listRequests;

  useEffect(() => {
    getRequests(filters).then(setListRequests);
  }, [getRequests, setListRequests])

  return (
    <TableContainer
      component={Paper}
      sx={{
        background: '#fff',
        boxShadow: '2px 2px 5px #0005',
        borderRadius: 2,
        px: 2,
        pb: 2,
      }}
    >
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow
            sx={{
              '& th': {
                color: 'var(--box-secondary)',
                fontWeight: 'bolder',
                py: 1.5,
                fontSize: '1rem',
              }
            }}
          >
            <TableCell>Codigo</TableCell>
            <TableCell align='right'>Nombre</TableCell>
            <TableCell align='right'>Prioridad</TableCell>
            <TableCell align='right'>Empresa</TableCell>
            <TableCell align='right'>Estado</TableCell>
            <TableCell align='center'>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.id}
              sx={{
                '&:hover': { background: 'rgba(0, 0, 0, .1)' },
                '& td': { py: 3 },
                '&:last-child td, &:last-child th': { border: 0 },
                position: 'relative',
              }}
            >
              <TableCell component="th" scope="row">
                {row.code}
              </TableCell>
              <TableCell align='right'>{row.name}</TableCell>
              <TableCell align='right'>{row.name_pri}</TableCell>
              <TableCell align='right'>{row.company_tradename}</TableCell>
              <TableCell align='right'>{row.name_sta}</TableCell>
              <TableCell>
                <ButtonActions dataRequest={row} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}