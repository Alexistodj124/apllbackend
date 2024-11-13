"""Add many-to-many relationship between Orden and Inventario

Revision ID: 2e443435f6fc
Revises: cda75e639b49
Create Date: 2024-11-11 23:21:55.280171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e443435f6fc'
down_revision = 'cda75e639b49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.create_table('orden_inventario',
    sa.Column('orden_id', sa.Integer(), nullable=False),
    sa.Column('inventario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inventario_id'], ['inventario.id'], ),
    sa.ForeignKeyConstraint(['orden_id'], ['orden.id'], ),
    sa.PrimaryKeyConstraint('orden_id', 'inventario_id')
    )
    op.drop_table('estados')
    op.drop_table('categoria')
    op.drop_table('persona')
    with op.batch_alter_table('carro', schema=None) as batch_op:
        batch_op.drop_column('edicion')

    with op.batch_alter_table('empleado', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('apellido', sa.String(length=100), nullable=False))
        batch_op.alter_column('id_usuario',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('id_persona')

    with op.batch_alter_table('inventario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repuesto', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('ingresados', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('vendidos', sa.Integer(), nullable=False))
        batch_op.alter_column('id_carro',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('precio_unitario',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
        batch_op.drop_constraint('inventario_bodega_fkey', type_='foreignkey')
        batch_op.drop_constraint('inventario_estado_fkey', type_='foreignkey')
        batch_op.drop_constraint('inventario_categoria_fkey', type_='foreignkey')
        batch_op.drop_column('categoria')
        batch_op.drop_column('bodega')
        batch_op.drop_column('stock')
        batch_op.drop_column('codigo_producto')
        batch_op.drop_column('dimension')
        batch_op.drop_column('estado')
        batch_op.drop_column('fabricante')

    with op.batch_alter_table('orden', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('vendedor_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('bodeguero_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'empleado', ['vendedor_id'], ['id'])
        batch_op.create_foreign_key(None, 'empleado', ['bodeguero_id'], ['id'])

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rol', sa.String(length=50), nullable=False))
        batch_op.create_unique_constraint(None, ['rol'])
        batch_op.drop_column('Rol')

    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('id_rol',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('id_rol',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Rol', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('rol')

    with op.batch_alter_table('orden', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('bodeguero_id')
        batch_op.drop_column('vendedor_id')
        batch_op.drop_column('fecha')

    with op.batch_alter_table('inventario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fabricante', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('estado', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('dimension', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('codigo_producto', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('stock', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('bodega', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('categoria', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('inventario_categoria_fkey', 'categoria', ['categoria'], ['id'])
        batch_op.create_foreign_key('inventario_estado_fkey', 'estados', ['estado'], ['id'])
        batch_op.create_foreign_key('inventario_bodega_fkey', 'bodega', ['bodega'], ['id'])
        batch_op.alter_column('precio_unitario',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
        batch_op.alter_column('id_carro',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('vendidos')
        batch_op.drop_column('ingresados')
        batch_op.drop_column('repuesto')

    with op.batch_alter_table('empleado', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_persona', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('id_usuario',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('apellido')
        batch_op.drop_column('nombre')

    with op.batch_alter_table('carro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('edicion', sa.VARCHAR(length=100), autoincrement=False, nullable=True))

    op.create_table('persona',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('dpi', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('nombre', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('apellido', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('edad', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('nit', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='persona_pkey')
    )
    op.create_table('categoria',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Categoria', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='categoria_pkey')
    )
    op.create_table('estados',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Estado', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='estados_pkey')
    )
    op.drop_table('orden_inventario')
    # ### end Alembic commands ###